def where_we_goin(ly):
 return ly*400

FL = 1500
FR = 1500
BL = 1500
BR = 1500

def left_right(ly):
  FL = 1500+where_we_goin(ly)
  FR = 1500-where_we_goin(ly)
  BL = 1500+where_we_goin(ly)
  BR = 1500-where_we_goin(ly)
  return FL, FR, BL, BR


def forward_backward(lx): 
    FL = 1500+where_we_goin(lx)
    FR = 1500+where_we_goin(lx)
    BL = 1500+where_we_goin(lx)
    BR = 1500+where_we_goin(lx)
    return FL, FR, BL, BR

def rotate(rx):
   FL = 1500-where_we_goin(rx)
   FR = 1500+where_we_goin(rx)
   BL = 1500-where_we_goin(rx)
   BR = 1500+where_we_goin(rx)
   return FL, FR, BL, BR
  
n = int(input())
print("If n is 1 then left, if n is -1 then right")
print(left_right(n))
print("If n is 1 then forward, if n is -1 then backward")
print(forward_backward(n))
print("If n is 1 then clockwise, if n is -1 then counterclockwise")
print(rotate(n))