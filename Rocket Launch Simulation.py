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
rocket.color("#C8C8C8")
rocket.penup()
rocket.setheading(90)

hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("white")
hud.goto(-290, 200)

c = turtle.Turtle()
c.hideturtle()
c.penup()
c.color("white")
c.goto(0,-250)

arc = turtle.Turtle()
arc.hideturtle()
arc.color("dim gray")
arc.fillcolor("dim gray")
arc.pensize(5)
arc.penup()
arc.goto(130, -300)
arc.setheading(90)
arc.pendown()
arc.begin_fill()
arc.circle(130, 180)
arc.forward(260)
arc.end_fill()

wn.update()

height = 0
speed = 0
gravity = -9.8
pixel_per_meter = 1
mass = 5
fuel = 100
fuel_burn = 1.2
max_thrust = 20

rocket.goto(0, height * pixel_per_meter)

def update_hud():
    hud.clear()
    hud.write(
        f"Speed: {speed:7.2f} m/s\n"
        f"Height: {height:7.2f} m\n"
        f"Acceleration: {acceleration:6.2f} m/s²\n"
        f"Fuel: {fuel:7.2f}%",
        font = ("Arial", 14, "bold")
    )

countdown_duration = 60     
start = time.perf_counter()
while True:
    elapsed = time.perf_counter() - start
    remaining = countdown_duration - elapsed

    if remaining <= 0:
        break

    mins, secs = divmod(int(remaining), 60)

    c.clear()
    c.write(
        f"T-{mins:02d}:{secs:02d}",
        align = "center",
        font = ("Courier", 24, "bold")
    )

    wn.update()
    time.sleep(0.01) 

c.clear()

flight_start = time.perf_counter()  
last_time = time.perf_counter()     

while True:
    now = time.perf_counter()
    dt = now - last_time
    last_time = now

    if dt > 0.1:
        dt = 0.1

    drag = -0.014 * speed * abs(speed)

    thrust = max_thrust * (fuel / 100)

    if height < 250 and speed < 0:
        desired_speed = -1
        error = desired_speed - speed
        thrust += error * 0.6
        if thrust > max_thrust:
            thrust = max_thrust

    acceleration = gravity + thrust + drag / mass

    speed += acceleration * dt
    height += speed * dt

    fuel_use = (thrust / max_thrust) * fuel_burn * dt
    fuel = max(0, fuel - fuel_use)

    flight_time = time.perf_counter() - flight_start
    mins, secs = divmod(int(flight_time), 60)

    c.clear()
    c.write(
        f"T+{mins:02d}:{secs:02d}",
        align = "center",
        font = ("Courier", 24, "bold")
    )

    if height <= 0:
        height = 0
        speed = 0
        acceleration = 0
        rocket.goto(0, 0)
        c.clear()
        c.write(
            "LANDING SUCCESS",
            align = "center",
            font = ("Arial", 15, "bold")
        )
        update_hud()
        wn.update()
        break

    rocket.goto(0, height * pixel_per_meter)
    update_hud()
    wn.update()

    time.sleep(0.001)

wn.mainloop()
