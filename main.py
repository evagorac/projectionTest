import numpy as np

def rotate_point(p, th, axis):
    s = np.sin(th)
    c = np.cos(th)
    r_matrix = None
    if axis == "x":
        r_matrix = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif axis == "y":
        r_matrix = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    elif axis == "z":
        r_matrix = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    if r_matrix is None:
        raise("Bruh {} is not valid".format(axis))
    return np.dot(r_matrix, p)

def scale(v, A, B, Ap, Bp):
    return (v-A)/(B-A) * (Bp-Ap) + Ap


intensity_map = " .:-=+*#%@"

h_camera_fov = 120  # degrees
v_camera_fov = 120  # degrees
focal_dist = 1
screen_dim = (100, 50)
camera_dist = 10

camera_pos = np.array([[camera_dist], [0], [0]])
camera_dir = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
camera_pose = np.block([[camera_dir, camera_pos], [np.zeros((1, 3)), np.ones((1, 1))]])

meat_r = .5
major_r = 2
circle_steps = 25
sweep_steps = 75

# cols xyz points
# rows for each point
base_circle = []

# contains torus
base_torus = []

# make circle
for i in range(circle_steps):
    th = i * 2 * np.pi / circle_steps
    point = np.array([[major_r + meat_r * np.cos(th)], [0], [meat_r * np.sin(th)]])
    base_circle.append(point)

# make torus
for p in base_circle:
    for i in range(sweep_steps):
        th = i * 2 * np.pi / sweep_steps
        base_torus.append(rotate_point(p, th, "z"))

def drawframe(transformed_torus):
    # first put torus in camera frame
    camera_torus = []
    for p in transformed_torus:
        temp = np.dot(camera_pose, np.vstack([p, np.ones((1, 1))]))
        camera_torus.append(temp[:3, 0].reshape((-1, 1)))

    # initialize screen
    screen = []
    for _ in range(screen_dim[1]):
        # screen.append([[0]] * screen_dim[0])
        screen.append([0] * screen_dim[0])

    # project points to screen
    for p in camera_torus:
        x, y, z = p[:, 0]
        scaling_factor = focal_dist / x
        if x < focal_dist:
            continue
        p_y = y * scaling_factor
        p_z = z * scaling_factor

        h_pixels_per_unit = screen_dim[0] / (2 * focal_dist * np.tan(h_camera_fov/2))
        v_pixels_per_unit = screen_dim[1] / (2 * focal_dist * np.tan(v_camera_fov / 2))

        row = -int(p_z * v_pixels_per_unit - screen_dim[1]/2)
        col = -int(p_y * h_pixels_per_unit - screen_dim[0]/2)

        try:
            brightness = int(scale(x, camera_dist - 2 * (meat_r + major_r), camera_dist + 2 * (meat_r + major_r), len(intensity_map), 0))
            # screen[row][col].append(brightness)
            if screen[row][col] < brightness:
                screen[row][col] = brightness
        except:
            pass
    # for row in screen:
    #     print(row)

    # for row in screen:
    #     line = ""
    #     for pixel_buffer in row:
    #         # each pixel in pixel buffer is tuple like ("value", brightness)
    #         max_brightness = pixel_buffer[0]
    #         for pixel_brightness in pixel_buffer:
    #             if pixel_brightness > max_brightness:
    #                 max_brightness = pixel_brightness
    #         line = line + intensity_map[max_brightness]
    #     print(line)

    for row in screen:
        line = ""
        for pixel in row:
            line = line + intensity_map[pixel]
        print(line)


# fill console with blanks to avoid screen glitching when starting up
for x in range(10000):
    print("Please wait while I spam the console")

# transform and draw torus
while(True):
    spin_steps = 100
    for step in range(spin_steps):
        torus = []
        th = step * 2 * np.pi / spin_steps
        for p in base_torus:
            torus.append(rotate_point(rotate_point(rotate_point(p, 3 * th, 'y'), 2 * th, 'x'), th, 'z'))
        drawframe(torus)

