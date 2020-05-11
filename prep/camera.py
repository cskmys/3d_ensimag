import numpy as np
import transform as t

YAW = -90.0
PITCH = 0.0
SPEED = 0.05
SENSITIVITY = 0.075
ZOOM = 45.0


class Camera:
    def __init__(self, position=t.vec(0.0, 0.0, 0.0), up=t.vec(0.0, 1.0, 0.0), yaw=YAW, pitch=PITCH):
        self.Position = position
        self.Front = t.vec(0.0, 0.0, -1.0)
        self.Up = None
        self.Right = None
        self.WorldUp = up

        self.Yaw = yaw
        self.Pitch = pitch
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM

        self._upd_cam_vec()

    def get_view_matrix(self):
        return t.lookat(self.Position, self.Position + self.Front, self.Up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.MovementSpeed * delta_time
        if direction == 'FORWARD':
            self.Position += self.Front * velocity
        if direction == 'BACKWARD':
            self.Position -= self.Front * velocity
        if direction == 'LEFT':
            self.Position -= self.Right * velocity
        if direction == 'RIGHT':
            self.Position += self.Right * velocity

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.MouseSensitivity
        yoffset *= self.MouseSensitivity

        self.Yaw += xoffset
        self.Pitch += yoffset

        if constrain_pitch:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0
        self._upd_cam_vec()

    def process_mouse_scroll(self, yoffset):
        self.Zoom -= yoffset
        if self.Zoom <= 1.0:
            self.Zoom = 1.0
        if self.Zoom >= 45.0:
            self.Zoom = 45.0

    def _upd_cam_vec(self):
        front_x = np.cos(np.radians(self.Yaw)) * np.cos(np.radians(self.Pitch))
        front_y = np.sin(np.radians(self.Pitch))
        front_z = np.sin(np.radians(self.Yaw)) * np.cos(np.radians(self.Pitch))
        self.Front = t.normalized(t.vec(front_x, front_y, front_z))
        self.Right = t.normalized(np.cross(self.Front, self.WorldUp))
        self.Up = t.normalized(np.cross(self.Right, self.Front))


def init_camera(position=t.vec(0.0, 0.0, 0.0), up=t.vec(0.0, 1.0, 0.0), yaw=YAW, pitch=PITCH):
    global camera
    camera = Camera(position, up, yaw, pitch)
    return camera


def get_camera_position():
    return camera.Position


def get_camera_direction():
    return camera.Front