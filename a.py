
# data: list = [ 
#     {
#         "source": "sp1",
#         "firstgrid": 1,
#         "textures": [1,1,1,1,1]
#     },
#     {
#         "source": "sp2",
#         "firstgrid": 6,
#         "textures": [2,2]
#     },
#     {
#         "source": "sp3",
#         "firstgrid": 8,
#         "textures": [3,3,3]
#     }
# ]
# sets: dict = {}

# for each in data:
#     source    = each["source"]
#     firstgrid = each["firstgrid"]
#     textures  = each["textures"]

    
#     # sets[source] = [(i,x) for i,x in enumerate([e for e in range(firstgrid + len(textures)])[firstgrid::]))]
#     sets[source] = [{x: i} for i,x in enumerate([e for e in range(firstgrid + len(textures))][firstgrid::])]

# print(sets)

class A:
    b = 1

print(A().__class__.__name__)

