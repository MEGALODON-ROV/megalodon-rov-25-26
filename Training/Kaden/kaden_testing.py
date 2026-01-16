def thruster_output(Lx, Ly, Rx, A, B):
  base = 1500
  scale = 400

  # Horizontal thrusters
  FL = base + Ly*scale + Lx*scale - Rx*scale
  FR = base + Ly*scale - Lx*scale + Rx*scale
  BL = base + Ly*scale - Lx*scale - Rx*scale
  BR = base + Ly*scale + Lx*scale + Rx*scale

  # Vertical thrusters
  vert = (A - B) * scale
  VFL = VFR = VBL = VBR = base + vert

  thrusters = [FL, FR, BL, BR, VFL, VFR, VBL, VBR]
  # make thrusters 1100-1900
  forsure = []
  for t in thrusters:
      if t > 1900:
          forsure.append(1900)
      elif t < 1100:
          forsure.append(1100)
      else:
          forsure.append(int(t))
  thrusters = forsure

  # Format output
  horiz = f"{thrusters[0]}-{thrusters[1]}={thrusters[2]}+{thrusters[3]}"
  vert  = f"{thrusters[4]},{thrusters[5]}]{thrusters[6]}/{thrusters[7]}"
  return horiz + "*" + vert
