---
layout: post
title: Securitization of Binary Gambling
date: May 24, 2021
time: 0:00 UTC-4
---

A securitization of sports betting would natually entail that equal risk is put to each outcome. A market would engulf the same amount of risk on each side of the bet.

# Introduction

It's worth mentioning how I crossed this. I had some curiosity into high frequency trading sports lines. I collected lines by the minute for a bit, and will continue to work on that, as I have a suspicion that sports lines move stochastically. If the lines move in some random fashion with high enough variance, then taking some positions at the beginning of the game, and counterwagering when profitable by some margin to effectively close the position could work. As specifically in basketball games, it's very uncommon to have monotonic line movements. Games are very much back and forth, and if the variance is high enough, overcoming the house edge should occur with some calculatable probability at some point in the game(finding the distribution line movements follow would be key, and I would wager this would seem close to a normal distribution with decay towards 0 and 1 as the game gets closer to the end). This effectively is opening a position, or multiple positions on a game, and then constantly hedging these bets. Say the odds of a 15% profitable counter wager coming up is over 85%, then this strategy has a positive EV. On working with that, I found what I believe to be a solution to the marketable sports bet. I am not sure how possible this idea is, however it lead me down a way to securitize and effectively close the spread sportsbooks constantly deal with.

Some terms worth defining. Moneyline is the amount required to win a certain amount. A positive moneyline +x, means for every \$100 wagered, you will win \$x on top of receiving your bet back. A negative moneyline -x, means for every \$x wagered, you will win \$100 on top of receiving your bet back. These are just another way of defining the odds $$x:y$$ or implied probabilities $$(0, 1)$$.

# Use Case for Individuals

Say the sportsbooks have the lines -110 and -110 for each outcome. Now two betters enter the market, Adam and Sarah. Adam would like to take the line for Team A to win the game. He could open a \$11 bet on the sportsbook and have potential winnings of \$21. Sarah wants to take the line for Team B to win the game. However she wants to take +100 on the game. Adam would rather take the bet with Sarah to increase his potential winnings on the same amount of risk, as he would open a line with Sarah for +100. Now it can be very difficult for Adam and Sarah to ever meet. And a market of thousands of different lines and handicaps with differing odds can be unwieldy. Instead we can create a market with a standardized security, or in this case contract. That can be traded in the same way an options contract is traded. We have two ways to create positions. Either two "market makers" or in this case betters come to agreement on the cost, effectively the lines, and create a new contract. Or someone is looking to exit their position, for a loss/gain/etc, and they can sell this contract on a marketplace where someone may want to take over the position. We'll first go over the first secenario. Adam will place a bid on a contract that will pay \$10 in the event Team A wins, and expire worthless if Team B wins at \$5. Sarah will see this offer on the marketplace and when she goes to "buy" the opposite end for \$5, in effect she is actually short selling, and the market will see this and create a contract with \$10 in escrow. Instead of a traditional contract where the underwriter is trusted to pay in the particular outcome, she will put up only the collateral sans Adam's bid.

In the event where Charlie would like to bet on Team B, and Sarah would like to exit her position, a similar series of events occur. Sarah will buy a new contract at \$7, effectively exiting by counterwagering at -223 moneyline, and Charlie will take the same position as Sarah did. Effectively Sarah has exited her position for a loss of \$2 by opening two contracts where one will be the collateral for the other and in the opposite outcome the payouts will just be 0. Charlie has entered his position at +233 and will wager \$3 to win \$10 in the case Team B wins. In a realistic scenario, this would be like Team A taking a large lead at half time.

Say another bidder, Donald, wants to take a position that Team A will win. And Adam would like to exit his position. In this event, there does not need to be another contract underwritten. Adam sells his contract to Donald for \$7, locking in a \$2 profit. This could be Adam deciding that Team B will win with a second half comeback, or just locking in his profits.

# Use Case for Sportsbooks

In the case for sportsbooks. They may want to make sure their books are balanced with an ideal house edge, they also would like to prevent arbitrage from occurring. When sportsbook A has an imbalancement, and moving the line may create arbitrage opportunities, they may call sportsbook B who may have the opposite issue. There is clearly an imbalance in negotiation power according to who has the least exposure. Instead they may want to balance their books respectively in a highly competitive market. Moving the lines will work for a specific book, and I would assume arbitrage is closed among the bookkeepers as opportunities arise so infrequently. In the event of an open market, this would effectively give bookkeepers the most effective way to close their exposures. I would assume this securitization may be too difficult for most sports betters, but leaders in the industry, who already quantitatively look at the sports betting market, may have a great way to cost effectively erase any imbalances in their books.

# Implementation

This would be effectively identical to markets in all other aspects. Except because they are binary options, and the events are the same, unlike calls and puts, one action is buying, and the opposite is selling or underwriting. It would follow the same algorithms and implementation details that CBOE and NYSE use would work. The only addition would likely be market making being done by some central arbiter, deciding to sell, or underwrite new contracts according to what positions are being made. It would effectively follow similarly to the above 3 scenarios in most cases, and deciding which side to make Team A and B, or which outcome is underwritten in itself can be chosen arbitrarily with effectively no risk to any party. Forward facing would be effectively to the user as opening and closing positions at two different prices whose sums are effectively \$10 or whatever the contract size is decided. The choice of \$10 was that it gives a wide range of possible money lines by increments of a penny.

# Blockchain

These same contracts can be created similarly with a blockchain. A unit, or coin can be divided infinitely barring 64 bit integer limitations. So contract size can be greatly reduced, while securing on some cryptographic ledger. I think detailing this in a white paper can be beneficial at some point. However the gist would be somewhat along the lines of a sidechain of say Ethereum. Someone can open a contract for their position. A contract consisting of their coin put in escrow by some script that will be 2 of 3 signature schemed with a central party arbiter. Along with their contract, they will sign a transaction releasing from escrow the funds, as well as the other side of the bet. Then the same positions and actions can be taken as above, however with less involvement of a central arbiter. The two parties can enter the agreement and sign their own transactions releasing the escrow funds to themselves in the two outcomes. Then the central arbiter can signify which action was taken, perhaps without the 2 of 3 signature scheme, and instead the script or transaction releasing the funds can be tied to some action the central arbiter takes, say a "integral transaction" that has two outcomes, then the central arbiter takes one. The same entering in and out of positions can be made with creating new contracts that are based on the "integral transaction" or based on the original transaction with the seller still leaving the original funds in the escrow but pocketing other escrow. In the event of making a new contract, instead what can occur is there is a risk free swap. As in the original contract is tied as the escrow in the event the seller is trying to exit, and otherwise the contract expires worthless.

This may become incredibly tied into each other and fidgety, but record keeping is easy for computers, and accurate along blockchains or other ledgers. The standardization of a contract, or securitization allows for easily swappable positions.

## Issues

The main issue would be in the event of a cancellation. In a normal world, people would get their money returned. However, as lines move, the values at stake can become very imbalanced. As in, If player A enters a contract with player B at \$5 each, then player C buys player A's position for $8, player A would make a profit of \$3, but then player B and C are now \$13 in capital where only \$10 exists. Easy solutions would be equal push in the event of a cancellation, or record keeping to the original bets made. But this would change the odds that the favorites will have a better payout than purely what the market would enforce. Or the market would incorporate this and have a slight bias towards the \$5 marker for both outcomes and imply some probability towards a push. Or you can introduce a third contract holder to the mix, but then this would make match making even more difficult as you would now need to find 3 holders all in the same.

A more workable solution would be along the lines of all contracts held in escrow, including swapped positions, so that in the event of a third outcome, all collateral is released to the original parties. This would reduce much of the necessary bookkeeping, but would lock funds throughout the entire game, which happens to be the case in most sportsbook already, but was originally an outcome I tried to avoid but have yet to come up with a solution.

# Odds Conversions

| Cost of Contract | Buy Equivalent Money Line | Implied Probability | Sell Equivalent Money Line | Implied Probability |
|---|---|---|---|---|
|$0.01|+99900|0.10%|-99900|99.90%
|$0.02|+49900|0.20%|-49900|99.80%
|$0.03|+33233|0.30%|-33233|99.70%
|$0.04|+24900|0.40%|-24900|99.60%
|$0.50|+1900|5.00%|-1900|95.00%
|$1.00|+900|10.00%|-900|90.00%
|$1.50|+567|15.00%|-567|85.00%
|$2.00|+400|20.00%|-400|80.00%
|$2.50|+300|25.00%|-300|75.00%
|$3.00|+233|30.00%|-233|70.00%
|$3.10|+223|31.00%|-223|69.00%
|$3.20|+212|32.00%|-212|68.00%
|$3.30|+203|33.00%|-203|67.00%
|$3.40|+194|34.00%|-194|66.00%
|$3.50|+186|35.00%|-186|65.00%
|$3.60|+178|36.00%|-178|64.00%
|$3.70|+170|37.00%|-170|63.00%
|$3.80|+163|38.00%|-163|62.00%
|$3.90|+156|39.00%|-156|61.00%
|$4.00|+150|40.00%|-150|60.00%
|$4.10|+144|41.00%|-144|59.00%
|$4.20|+138|42.00%|-138|58.00%
|$4.30|+133|43.00%|-133|57.00%
|$4.40|+127|44.00%|-127|56.00%
|$4.50|+122|45.00%|-122|55.00%
|$4.51|+122|45.10%|-122|54.90%
|$4.52|+121|45.20%|-121|54.80%
|$4.53|+121|45.30%|-121|54.70%
|$4.54|+120|45.40%|-120|54.60%
|$4.55|+120|45.50%|-120|54.50%
|$4.56|+119|45.60%|-119|54.40%
|$4.57|+119|45.70%|-119|54.30%
|$4.58|+118|45.80%|-118|54.20%
|$4.59|+118|45.90%|-118|54.10%
|$4.60|+117|46.00%|-117|54.00%
|$4.61|+117|46.10%|-117|53.90%
|$4.62|+116|46.20%|-116|53.80%
|$4.63|+116|46.30%|-116|53.70%
|$4.64|+116|46.40%|-116|53.60%
|$4.65|+115|46.50%|-115|53.50%
|$4.66|+115|46.60%|-115|53.40%
|$4.67|+114|46.70%|-114|53.30%
|$4.68|+114|46.80%|-114|53.20%
|$4.69|+113|46.90%|-113|53.10%
|$4.70|+113|47.00%|-113|53.00%
|$4.71|+112|47.10%|-112|52.90%
|$4.72|+112|47.20%|-112|52.80%
|$4.73|+111|47.30%|-111|52.70%
|$4.74|+111|47.40%|-111|52.60%
|$4.75|+111|47.50%|-111|52.50%
|$4.76|+110|47.60%|-110|52.40%
|$4.77|+110|47.70%|-110|52.30%
|$4.78|+109|47.80%|-109|52.20%
|$4.79|+109|47.90%|-109|52.10%
|$4.80|+108|48.00%|-108|52.00%
|$4.81|+108|48.10%|-108|51.90%
|$4.82|+107|48.20%|-107|51.80%
|$4.83|+107|48.30%|-107|51.70%
|$4.84|+107|48.40%|-107|51.60%
|$4.85|+106|48.50%|-106|51.50%
|$4.86|+106|48.60%|-106|51.40%
|$4.87|+105|48.70%|-105|51.30%
|$4.88|+105|48.80%|-105|51.20%
|$4.89|+104|48.90%|-104|51.10%
|$4.90|+104|49.00%|-104|51.00%
|$4.91|+104|49.10%|-104|50.90%
|$4.92|+103|49.20%|-103|50.80%
|$4.93|+103|49.30%|-103|50.70%
|$4.94|+102|49.40%|-102|50.60%
|$4.95|+102|49.50%|-102|50.50%
|$4.96|+102|49.60%|-102|50.40%
|$4.97|+101|49.70%|-101|50.30%
|$4.98|+101|49.80%|-101|50.20%
|$4.99|+100|49.90%|-100|50.10%
|$5.00|+100|50.00%|-100|50.00%
|$5.01|-100|50.10%|+100|49.90%
|$5.02|-101|50.20%|+101|49.80%
|$5.03|-101|50.30%|+101|49.70%
|$5.04|-102|50.40%|+102|49.60%
|$5.05|-102|50.50%|+102|49.50%
|$5.06|-102|50.60%|+102|49.40%
|$5.07|-103|50.70%|+103|49.30%
|$5.08|-103|50.80%|+103|49.20%
|$5.09|-104|50.90%|+104|49.10%
|$5.10|-104|51.00%|+104|49.00%
|$5.11|-104|51.10%|+104|48.90%
|$5.12|-105|51.20%|+105|48.80%
|$5.13|-105|51.30%|+105|48.70%
|$5.14|-106|51.40%|+106|48.60%
|$5.15|-106|51.50%|+106|48.50%
|$5.16|-107|51.60%|+107|48.40%
|$5.17|-107|51.70%|+107|48.30%
|$5.18|-107|51.80%|+107|48.20%
|$5.19|-108|51.90%|+108|48.10%
|$5.20|-108|52.00%|+108|48.00%
|$5.21|-109|52.10%|+109|47.90%
|$5.22|-109|52.20%|+109|47.80%
|$5.23|-110|52.30%|+110|47.70%
|$5.24|-110|52.40%|+110|47.60%
|$5.25|-111|52.50%|+111|47.50%
|$5.26|-111|52.60%|+111|47.40%
|$5.27|-111|52.70%|+111|47.30%
|$5.28|-112|52.80%|+112|47.20%
|$5.29|-112|52.90%|+112|47.10%
|$5.30|-113|53.00%|+113|47.00%
|$5.31|-113|53.10%|+113|46.90%
|$5.32|-114|53.20%|+114|46.80%
|$5.33|-114|53.30%|+114|46.70%
|$5.34|-115|53.40%|+115|46.60%
|$5.35|-115|53.50%|+115|46.50%
|$5.36|-116|53.60%|+116|46.40%
|$5.37|-116|53.70%|+116|46.30%
|$5.38|-116|53.80%|+116|46.20%
|$5.39|-117|53.90%|+117|46.10%
|$5.40|-117|54.00%|+117|46.00%
|$5.41|-118|54.10%|+118|45.90%
|$5.42|-118|54.20%|+118|45.80%
|$5.43|-119|54.30%|+119|45.70%
|$5.44|-119|54.40%|+119|45.60%
|$5.45|-120|54.50%|+120|45.50%
|$5.46|-120|54.60%|+120|45.40%
|$5.47|-121|54.70%|+121|45.30%
|$5.48|-121|54.80%|+121|45.20%
|$5.49|-122|54.90%|+122|45.10%
|$5.50|-122|55.00%|+122|45.00%
|$5.60|-127|56.00%|+127|44.00%
|$5.70|-133|57.00%|+133|43.00%
|$5.80|-138|58.00%|+138|42.00%
|$5.90|-144|59.00%|+144|41.00%
|$6.00|-150|60.00%|+150|40.00%
|$6.10|-156|61.00%|+156|39.00%
|$6.20|-163|62.00%|+163|38.00%
|$6.30|-170|63.00%|+170|37.00%
|$6.40|-178|64.00%|+178|36.00%
|$6.50|-186|65.00%|+186|35.00%
|$6.60|-194|66.00%|+194|34.00%
|$6.70|-203|67.00%|+203|33.00%
|$6.80|-212|68.00%|+212|32.00%
|$6.90|-223|69.00%|+223|31.00%
|$7.00|-233|70.00%|+233|30.00%
|$7.50|-300|75.00%|+300|25.00%
|$8.00|-400|80.00%|+400|20.00%
|$8.50|-567|85.00%|+567|15.00%
|$9.00|-900|90.00%|+900|10.00%
|$9.50|-1900|95.00%|+1900|5.00%
|$9.96|-24900|99.60%|+24900|0.40%
|$9.97|-33233|99.70%|+33233|0.30%
|$9.98|-49900|99.80%|+49900|0.20%
|$9.99|-99900|99.90%|+99900|0.10%
