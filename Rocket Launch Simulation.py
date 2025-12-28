import turtle
import time
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)
wn.delay(0)

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
hud.speed(0)

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
acceleration = 0
pixel_per_meter = 1
fuel = 100
max_thrust = 900
dry_mass = 40
fuel_mass_full = 20
earth_radius = 6371000
rho0 = 1.225
drag_k = 0.014
exhaust_velocity = 4000
Kp = 6
Kd = 3
desired_speed = 0
last_error = 0
fuel_reverse = 10
landing_height_trigger = 250
landing_target_speed = -5

rocket.goto(0, height * pixel_per_meter)

def rocket_mass(fuel_percent):
    fuel_mass = (fuel_percent / 100) * fuel_mass_full
    return dry_mass + fuel_mass

def update_hud():
    hud.clear()
    hud.goto(-290, 200)
    hud.write(
        f"Speed: {speed:7.2f} m/s\n"
        f"Height: {height:7.2f} m\n"
        f"Acceleration: {acceleration:6.2f} m/s²\n"
        f"Fuel: {fuel:7.2f}%",
        font=("Arial", 14, "bold")
    )

countdown_duration = 30
start = time.perf_counter()
while True:
    elapsed = time.perf_counter() - start
    remaining = countdown_duration - elapsed
    if remaining <= 0:
        break
    mins, secs = divmod(int(remaining), 60)
    c.clear()
    c.goto(0, -250)
    c.write(f"T-{mins:02d}:{secs:02d}", align="center", font=("Courier", 24, "bold"))
    wn.update()
    time.sleep(0.01)

c.clear()
last_hud_update = 0
flight_start = time.perf_counter()
last_time = time.perf_counter()

while True:
    now = time.perf_counter()
    dt = now - last_time
    last_time = now
    if dt > 0.1:
        dt = 0.1

    mass = rocket_mass(fuel)
    g = -9.8 * (earth_radius / (earth_radius + height)) **2
    density = rho0 * math.exp(-height / 8000)
    drag = -drag_k * density * speed * abs(speed)
    thrust = 0

    if fuel > fuel_reverse:
        if height < 3000:
            thrust = max_thrust * 0.7
        elif height < 7000:
            thrust = max_thrust * 0.35
        else:
            thrust = max_thrust * 0.15

    if height < landing_height_trigger and speed < 0:
        desired_speed = landing_target_speed
        error = desired_speed - speed
        derivative = (error - last_error) / dt
        thrust = max(0, min(max_thrust, Kp * error + Kd * derivative))
    else:
        if speed >= 0:
            desired_speed = speed
        else:
            if height > 1500:
                desired_speed = -120
            elif height > 800:
                desired_speed = -50
            elif height > 400:
                desired_speed = -25
            elif height > 200:
                desired_speed = -10
            else:
                desired_speed = -3
        error = desired_speed - speed
        derivative = (error - last_error) / dt
        thrust_correction = Kp * error + Kd * derivative
        thrust += thrust_correction
        last_error = error

    thrust = max(0, min(thrust, max_thrust))
    acceleration = g + (thrust / mass) + (drag / mass)
    speed += acceleration * dt
    height += speed * dt
    fuel_mass = (fuel / 100) * fuel_mass_full
    mass_flow = thrust / exhaust_velocity
    fuel_mass = max(0, fuel_mass - mass_flow * dt)
    fuel = (fuel_mass / fuel_mass_full) * 100
    flight_time = time.perf_counter() - flight_start
    mins, secs = divmod(int(flight_time), 60)
    c.clear()
    c.write(f"T+{mins:02d}:{secs:02d}", align="center", font=("Courier", 24, "bold"))

    if height <= 0:
        height = 0
        speed = 0
        acceleration = 0
        rocket.goto(0, 0)
        c.clear()
        c.write("LANDING SUCCESS", align="center", font=("Arial", 15, "bold"))
        update_hud()
        wn.update()
        break

    rocket.goto(0, height * pixel_per_meter)
    if now - last_hud_update > 0.05:
        update_hud()
        last_hud_update = now

    wn.update()
    time.sleep(0.001)

wn.mainloop()
