import turtle
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

ground = turtle.Turtle()
ground.hideturtle()
ground.penup()
ground.goto(-300, -8)  
ground.pendown()
ground.color("green")
ground.begin_fill()
ground.setheading(270) 
ground.forward(300)       
ground.setheading(0)     
ground.forward(600)       
ground.setheading(90)    
ground.forward(300)      
ground.setheading(180)   
ground.forward(600)      
ground.end_fill()

rocket = turtle.Turtle()
rocket.shape("triangle")  
rocket.color("blue")
rocket.penup()
rocket.setheading(90)

hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("white")
hud.goto(-290, 180)

height = 0                 
speed = 100             
gravity = -9.8
time_step = 0.02
t = 0
pixel_per_meter = 0.4
mass = 5
fuel = 100
fuel_burn = 1.2
max_thrust = 15

rocket.goto(0, height * pixel_per_meter)

def update_hud():
    hud.clear()
    hud.write(
        f"Time: {t:.1f} s\n"
        f"Speed: {speed:.2f} m/s\n"
        f"Height: {height:.2f} m\n"
        f"Acceleration: {acceleration:.2f} m/s²\n"
        f"Fuel: {fuel:.2f}%",
        font = ("Arial", 14, "bold")
    )   

while True:
    drag = -0.014 * speed * abs(speed)
    thrust = max_thrust * (fuel / 100)
    acceleration = gravity + thrust + drag / mass
    speed = speed + acceleration * time_step
    height = height + speed * time_step
    t += time_step
    fuel = max(0, fuel - fuel_burn * time_step)

    if height <= 0:
        height = 0
        rocket.goto(0, height * pixel_per_meter)
        update_hud()
        wn.update()
        break

    rocket.goto(0, height * pixel_per_meter)
    update_hud()
    wn.update()
    time.sleep(0.02)

wn.mainloop()

