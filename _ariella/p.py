x = """
AA_Page1_AB.html
A_Final_AB.css
All_Images_lab_3
All_Images_lab4_AB
All_Index_AB.html
A_MyTemplate_AB.html
A_page2_AB.html
A_page3_AB.html
bdog.jpeg
blcat.jpeg
business.jpeg
cat.jpeg
cocky.jpeg
coliseum.jpeg
<!DOCTYPE html>.html
elephant.jpeg
family.jpg
geyser1.jpeg
geyser1resize.jpg
geyser2.jpeg
geyser2resize.jpg
grand2.jpeg
grand.jpeg
halloween1.jpg
hibiscus.jpeg
hi.html
homefriend.JPG
horseshoe.jpg
hw3test.html
hydflower.jpeg
index.md
Lab10aAB.html
Lab10bAB.html
Lab11aAB.html
Lab11bAB.html
Lab12AB.html
Lab13aAB.html
lab2AB.html
lab3Aab.html
lab3Bab.html
Lab4AAB.html
lab5AAB.html
lab5a.css
lab5B1ab.html
lab5B2ab.html
lab5Bab.css
Lab6ab.html
Lab7aAB.html
Lab7bAB.html
Lab888.html
Lab8AAB.html
Lab8B1AB.html
Lab8B2AB.html
Lab9aAB.html
Lab9bAB.html
LabB4AB.html
leaves.jpeg
library.jpg
life.jpeg
lily.jpeg
me.JPG
oldfaithful.jpeg
oldfaithfulresize.jpg
oldf.jpeg
paint1.jpeg
paint2.jpeg
paint3.jpeg
paint4.jpeg
pool1.jpeg
pool1resize.jpg
pool2.jpeg
pool2resize.jpg
pretty.jpeg
ProjectFallp1.html
ProjectNavigation.html
ProjectTestPageAB.html
pumpkin.jpeg
schoolfriend.jpg
usc.jpeg
vote.jpg
yellow1.jpeg
yellow1resize.jpg
yellow2.jpeg
yellow2rezise.jpeg
yellow3.jpeg
yellow3resize.jpg
yellow4.jpeg
yellow4resize.jpg
"""
x = x.split()
for i in x:
  if not i.endswith("html"):
    continue
  print("<a href=\"%s\">%s</a><br>" % (i, i))
