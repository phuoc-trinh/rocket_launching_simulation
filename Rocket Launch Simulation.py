import turtle
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(width=600, height=600)

ground = turtle.Turtle()
ground.hideturtle()
ground.penup()
ground.goto(-300, -9)  
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

height = 0                 
speed = 50                 
gravity = -6
time_step = 0.2
t = 0

rocket.goto(0, height)

while True:
    speed = speed + gravity * time_step
    height = height + speed * time_step
    t = t + time_step

    if height <= 0:
        height = 0
        rocket.goto(0, height)
        print(f"Time: {t:.1f}, Speed: {speed:.1f}, Height: {height:.1f}")
        break

    rocket.goto(0, height)
    print(f"Time: {t:.1f}, Speed: {speed:.1f}, Height: {height:.1f}")
    time.sleep(0.1)

wn.mainloop()
