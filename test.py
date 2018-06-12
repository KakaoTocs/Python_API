# str = "http://cfile236.uf.daum.net/image/1368A4415130206E0CF59F.png"
#
# pc = 180
# end = int(pc/90)
# for i in range(0, end):
#     if ".jpg" not in str:
#         if ".png" not in str:
#             print("no have")
#         else:
#             print("png")
#     else:
#         print("jpg")

def add(a):
    a[0] = a[0] + 1
    print(a[0])

a = ([1, 2])
print(a[0])
add(a)
print(a[0])
