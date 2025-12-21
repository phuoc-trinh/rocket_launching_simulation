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
hud.goto(-280, 230)

height = 0                 
speed = 100                
gravity = -9.8
time_step = 0.02
t = 0
pixel_per_meter = 5
mass = 5

rocket.goto(0, height * pixel_per_meter)

while True:
    drag = -0.015 * speed * abs(speed)
    acceleration = gravity + drag / mass
    speed = speed + acceleration * time_step
    height = height + speed * time_step
    t += time_step

    if height <= 0:
        height = 0
        rocket.goto(0, height * pixel_per_meter)
        hud.clear()
        hud.write(
        f"Time: {t:.1f} s\nSpeed: {speed:.2f} m/s\nHeight: {height:.2f} m",
        font=("Arial", 14, "bold")  
        )
        wn.update()
        break

    rocket.goto(0, height * pixel_per_meter)
    hud.clear()
    hud.write(
    f"Time: {t:.1f} s\nSpeed: {speed:.2f} m/s\nHeight: {height:.2f} m",
    font=("Arial", 14, "bold")  
    )
    wn.update()
    time.sleep(0.02)

wn.mainloop()
