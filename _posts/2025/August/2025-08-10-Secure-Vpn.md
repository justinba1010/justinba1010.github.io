---
layout: post
title: Building a Secure Corporate VPN With Infrastructure As Code
date: August 10, 2025
time: 22:00 UTC-5
---

How we built a hybrid mesh VPN with Tailscale in just over a day, that requires
nearly no maintenance. See the original post
[here](https://yuzu.health/blog/secure-vpn-infra).


## Problem Statement

At any company there is always a need for secure networking for provisioning
access to databases, giving engineers privileged access to internal networks, or
just having internal services company wide. Traditionally, this would be done
with a VPN or SSH tunnels to specific servers with privileged network access.
This is not optimal, even once your team grows past 5 it becomes burdensome.
Maintaining either solution can grow to a full time job itself, and punching
holes in our office network and/or our virtual private cloud is very
error-prone. We would also need to provision separate solutions for each type of
access. Instead, we turned to
[Tailscale](https://tailscale.com/kb/1151/what-is-tailscale), which would allow
us to very quickly provision access to key internal services with minimal
operational work for engineers.

### Why Tailscale?

We chose Tailscale for 3 main reasons: ease of deployment, fine tooth access
control, and a 
[mesh network topology](https://en.wikipedia.org/wiki/Mesh_networking). 
The first is extremely important for us; we cannot invest too much bandwidth
into network security - we’re a startup, and there are just much bigger problems
in our day to day, whether we’re ensuring a member gets care as fast as
possible, or ensuring employers have high control over healthcare costs.
However, that doesn’t mean we can ignore it. We needed a solution that allowed
us to set it and forget it.


Secondly, fine tooth access control is incredibly necessary for scaling. It
allows us to pick a solution that we hopefully will never outgrow. Having access
control at this level means we can have differing levels of access for different
sets of engineers, it means we can host internal services like a suite of
document tools to maintain HIPAA compliance. It even means we can jokingly host
a Minecraft server for all employees by adding a single line to the ACL file.
Lastly, the mesh network topology means traffic is not being unnecessarily
routed, which costs time, between extreme ping when traveling; and money for
when that traffic ends up at our bastion.


Note: We already utilize IAM authentication for RDS to provision access control for database access. It is granular enough that engineers cannot alter, or create rows for certain tables(around auditability). Tailscale allows us to very easily maintain connectivity to these databases, and avoids us from ever exposing an unnecessary public attack vector.



## Network Topology

First we had to decide how we’d like to configure this. Obviously, when picking
a tool like Tailscale we wanted to lean into it’s design philosophy. We see
almost no latency, and all engineers keep the Tailscale client on practically
24/7, ensuring nearly no interruption with configuration, no adding SSH public
keys to a central bastion, no >250ms latency when working remotely from the west
coast.


We decided upon a few subnet routers for access to anything that lives inside our AWS VPCs.

![Network Topology](https://cdn.yuzu.health/d67cf217-42ba-4efc-a80c-eab54b0b9a61/image.png)

![Actual Network Topology](https://cdn.yuzu.health/068b7901-707f-4172-81db-832023df7d4d/image.png)


## Infrastructure As Code


We migrated from Pulumi to [CDK](https://aws.amazon.com/cdk/) for a handful of
reasons. Without getting too deep into them, the design patterns that the CDK
developers lay out allow much more robust and democratic dev-ops among
engineering teams. In most IaC tools you are designing a configuration: you need
to design each resource and it’s connections as configuration, not logical
units. CDK lets you design these as
[“constructs”](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html). You
can also compose and interweave constructs together to get “stacks”. Stacks are
an encapsulated “idea”, this abstraction isn’t along the cloud resources
themselves, but the business logic that is meant.


For example, the CDK code that will be published below will be for the TailscaleStack. This stack is meant to encapsulate all the resources needed for provisioning an EC2 instance, with connectivity to the desired resources, permissions, standing up Tailscale itself, and other services it will use.


```ts
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import type { Construct } from "constructs";

import { Ec2Instance } from "$constructs/ec2/index.ts";
import { DatabaseInstance } from "$constructs/rds/index.ts";
import { Stack, type StackProps } from "$constructs/yuzu/stack.ts";

export interface TailscaleStackProps extends StackProps {
  instanceClass: ec2.InstanceClass;
  instanceSize: ec2.InstanceSize;
  subnetRoutes: Routing[];
  databaseStacks: string[];
}

const GB = 1024 * 1024 * 1024;
/**
 * This stack is used to deploy a bastion host that is used to access the database.
 * It also deploys subnet routing for the internal services
 */
export class TailscaleStack extends Stack {
  constructor(scope: Construct, id: string, props: TailscaleStackProps) {
    const { instanceClass, instanceSize, subnetRoutes } = props;
    super(scope, id, props);

    const tailscaleSG = new ec2.SecurityGroup(this, "TailscaleSG", {
      vpc: this.vpc,
    });
    tailscaleSG.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.udp(41_641));
    tailscaleSG.addIngressRule(ec2.Peer.anyIpv6(), ec2.Port.udp(41_641));

    const tailscaleInstance = new Ec2Instance(this, "TailscaleInstance", {
      vpc: this.vpc,
      securityGroup: tailscaleSG,
      instanceType: ec2.InstanceType.of(instanceClass, instanceSize),
      userData: this.userDataTailscale(subnetRoutes),
      alarms: {
        network: {
          threshold: 15 * GB,
          alertEngineering: true,
        },
      },
    });

    tailscaleInstance.role.attachInlinePolicy(new iam.Policy(this, "TailscaleSSMAccess", {
        statements: tailscaleKeySSMStatement(this.accountId),
      }),
    );

    for (const databaseStack of props.databaseStacks) {
      const rdsSg = DatabaseInstance.importSecurityGroup(this, databaseStack);
      rdsSg.connections.allowFrom(tailscaleSg, ec2.Port.tcp(5432));
    }
  }

  private userDataTailscale(subnetRoutes: string[]) {
    const userData = ec2.UserData.forLinux();
    const tailscaleRefreshScript = `/usr/local/bin/tailscale_refresh.sh`;
    userData.addCommands(
      // Install Tailscale + Setup SubnetRouters + append to tailscaleRefreshScript for reuse
      `echo '*/10 * * * * root ${tailscaleRefreshScript}' | sudo tee -a /etc/crontab`,
      "sudo systemctl enable --now tailscaled",
    );
    return userData;
  }
}
```

This happens to be our only use of EC2 at Yuzu; we continue to favor
[ECS](https://aws.amazon.com/ecs/) services for their robust uptimes among many
other reasons. This showcases some of the strengths of CDK and in this case our
design patterns; notably here, Ec2Instance follows our pattern of passing the
alarm configurations to the services themselves.


This democratizes dev-ops among engineering teams. When the tools for developing
new services, and going from application → deploy are very logical and straight
forward, engineers feel empowered to carry projects from start to deploy. It
also makes all of our engineers more cognizant of what our infrastructure
picture is.

```
Resources
  [+] AWS::EC2::SecurityGroup TailscaleSG [...]
  [+] AWS::EC2::SecurityGroupIngress TailscaleSG/from [...]:80 [...]
  [+] AWS::EC2::SecurityGroupIngress TailscaleSG/from [...]:443 [...]
  [+] AWS::IAM::Role TailscaleInstance/InstanceRole [...]
  [+] AWS::IAM::InstanceProfile TailscaleInstance/InstanceProfile [...]
  [+] AWS::EC2::Instance TailscaleInstance [...]
  [+] AWS::CloudWatch::Alarm TailscaleInstance/CpuUtilizationAlarm [...]
  [+] AWS::CloudWatch::Alarm TailscaleInstance/NetworkInAlarm [...]
  [+] AWS::CloudWatch::Alarm TailscaleInstance/NetworkOutAlarm [...]
  [+] AWS::EC2::LaunchTemplate TailscaleInstance/LaunchTemplate [...]
  [+] AWS::IAM::Policy TailscaleSSMAccess [...]
  [+] AWS::EC2::SecurityGroupIngress DatabaseStackRdsSg/from [...]:5432 [...]
  [+] AWS::EC2::SecurityGroupIngress [...anotherDatabaseStack...]RdsSg/from [...]:5432 [...]
  [+] AWS::EC2::SecurityGroupIngress [...internalService1...]/from [...]:80 [...]
  [+] AWS::EC2::SecurityGroupIngress [...internalService1...]/from [...]:443 [...]
```

### Explanation

This stack configures an EC2 instance that acts as a [bastion
host](https://en.wikipedia.org/wiki/Bastion_host). It configures a [subnet
router](https://tailscale.com/kb/1019/subnets) which basically means it acts as
an exit node for selected routes(in this case internal services). It will
introduce selective connectivity between all devices in the
[Tailnet](https://tailscale.com/kb/1136/tailnet) (what Tailscale calls its VPN
equivalent) according to the ACL. We only included a rudimentary connectivity
example for RDS for brevity, but internally this is implemented similarly to how
alarms are written for all of our CDK constructs. Notably we can turn on flags
on our stack constructs to turn on connectivity with the Tailnet, then we pass
the CNAME records to the stack and our user data script will provision new
subnet routing on deploy, and update moving targets with the crontab refresh.

## Access Control

From here on out, we’re completely relying on Tailscale for access control. There are plenty of resources on this. A few examples on how we use Tailscale:

### SSH

We use Tailscale to avoid having to rotate and manage SSH public keys among all
of our shared resources. We have SSH enabled for managing those bastions and a
single host with a user for every engineer that manages miscellaneous internal
tooling.

```json
"ssh": [
// Allow users to access their provisioned user
// if they have a provisioned user
{
	"action": "accept",
	"src":    ["user:*@yuzu.health"],
	"dst":    ["tag:a_shared_ubuntu_box"],
	"users":  ["localpart:*@yuzu.health"],
},
// Allow access to owner devices
{
	"action": "accept",
	"src":    ["autogroup:member"],
	"dst":    ["autogroup:self"],
	"users":  ["autogroup:nonroot", "root"],
},
// Allow access to bastions
{
	"action": "accept",
	"src":    ["group:aws_admin"],
	"dst":    ["tag:bastion"],
	"users":  ["autogroup:nonroot", "ec2-user", "root"],
},
],
```

### SSH Access to Our Individually Provisioned User On A Shared Box

These advanced features are the most enticing features of Tailscale. We are able
to with just the first ssh rule above allow engineers to access very specific
per box controls. Although we do not utilize much infrastructure that are not
completely managed services, we do see this infinite extensibility being handy
in the long run.


```
➜  ~ ssh justin@yuzu-server  
Welcome to Yuzu Health (Running on Ubuntu 24.04.2 LTS)
                       .++.                        
  /\    /\ _________ +888888+                        
   \\  //  ---------+88888888+                      
    \\//            +88888888+                     
     ||              '888888'                     
     ||                '++'       
     \/                 || 
                        ||
     /\                 ||
     ||                 ||
     ||                 ||
     ||                 ||
     ||_________________||
     ++-----------------++

 * Documentation:      https://yuzu.health/docs
 * Top:                http://yuzu-server/
justin@Yuzu-Server:~$ ^d
logout
Connection to yuzu-server closed.
➜  ~ ssh pam@yuzu-server   
tailscale: failed to evaluate SSH policyConnection closed by 100.80.73.101 port 22
```


### Access to our RDS Instances/Clusters

```json
  "acls": [
		// Allow db access for engineers
		{
			"action": "accept",
			"src":    ["group:engineer"],
			"dst":    ["dev_database:5432"],
		},
]
```

We use IAM authentication for our RDS instance, and just for an example of all
of this together and how we connect to all of our RDS instances.


```
➜  ~ which psqldev
psqldev: aliased to PGPASSWORD="$(aws rds --profile dev generate-db-auth-token [...])" \
psql "host=[...] dbname=dev user=iam_readwrite sslmode=require"
➜  ~ psqldev
psql (17.5, server xx.xx)
SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, compression: off, ALPN: none)
Type "help" for help.

dev=> 
```

## Wrap Up

At Yuzu, we tackle a wide range of challenges every day. As a small,
high-velocity team, we thrive on problems that demand both inquisitive
exploration and decisive execution. Our engineers work across a diverse domain;
from applicational problems like claims ingestion, demographic matching, and web
development, to more abstract problems like maximal connected bipartite
subgraphs, database performance, and scheduling. And we don’t tackle these
problems in the theoretical sense, we’re solving them every day. If working on
an expansive set of problems interests you and you’ve made it this far; keep
scrolling and let us know what interested you in this blog post in your cover
letter. I will shamelessly plug our team at large, and especially our
engineering team as one of the most fun, exciting, and extremely
solutions-driven teams I’ve worked on.

![Company Photo](https://cdn.yuzu.health/4b3e4690-8372-48c2-a7ff-fd41451f64c9/image.png)