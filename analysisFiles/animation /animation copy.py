from vpython import *

# Scene setup
scene = canvas(title="Rotating Balls")
scene.width = 800
scene.height = 600

# Central line
axis = cylinder(pos=vector(-3, 0, 0), axis=vector(6, 0, 0), radius=0.1)

# Balls
balls = []
colors = [color.red, color.green, color.blue] 
positions = [vector(0, 2, 0), vector(0, 0, 0), vector(0, -2, 0)]

for i in range(3):
    balls.append(sphere(pos=positions[i], radius=0.4, color=colors[i]))

# Animation loop
dt = 0.01  # Time step
angular_speeds = [0.8, 1.2, 1.5]  # Different rotation speeds

while True:
    rate(100)  # Limit frame rate

    for i, ball in enumerate(balls):
        angle = angular_speeds[i] * dt
        ball.rotate(angle=angle, axis=axis.axis, origin=axis.pos)