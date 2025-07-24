"""

Here we try to answer questions like:

- How common is each level card?
- Visualize the distribution of deck levels?
- Visualize the distribution of board levels?
- Visualize the distribution of NLH hand levels?
- %ile ranking for starting hands in Level N deck
- %ile ranking for showdown categories in Level N deck

Opening hand chart:

Each deck has four cards per rank. In terms of level,
we can sort them Top, Upper, Lower, Bottom.

# # # # # # # # # # #
# Deck level: 6     #
# Best hand:        #
#                   #
# Xs Yd Zh Ah Bh    #
# # # # # # # # # # #

# # # # # # # # # # #
# Hand: [AA]        #
# Levels: 6432      #
#                   #
# tu% tl% tb%       #
#     ul% ub%       #
#         lb%       #
# # # # # # # # # # #

# # # # # # # # # # #
# Hand: [AKs]       #
# Levels: 6432+3254 #
#                   #
# t% u% l% b%       #
# # # # # # # # # # #

# # # # # # # # # # #
# Hand: [AKo]       #
# Levels 6432*5432  #
#                   #
# tt% tu% tl% tb%   #
# ut% uu% ul% ub%   #
# lt% lu% ll% lb%   #
# bt% bu% bl% bb%   #
# # # # # # # # # # #

If levels
are tied, we gray out the corresponding indicators. E.g.
if all aces are Level 2, we only have a top and upper 
ace.

# # # # # # # # # # #
# Hand: [AA]        #
# Levels: 2         #  
#                   #
# tu% t̶l̶%̶ t̶l̶%̶       #
#     t̶l̶%̶ t̶l̶%̶       #
#         t̶l̶%̶       #
# # # # # # # # # # #

"""
