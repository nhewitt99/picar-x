from time import sleep
import numpy as np
import cv2


class LaneCamera:
    from picamera import PiCamera

    """
    Class to estimate "lanes" i.e. tape
    Could add color heuristics later, but ignoring hue
    allows me to track black lines as well (which is better for
    my testing at home)
    """

    def __init__(self):
        # TODO: this could throw exceptions, might want some error catching
        self.cam = self.PiCamera()
        self.cam_setup()

        # Magic numbers from tutorials. Tune as needed.
        self.config = {
            "blur_size": (5, 5),
            "thresh_low": 50,
            "thresh_high": 150,
            "hough_rho": 2,
            "hough_theta": np.pi / 180,
            "hough_thresh": 100,
            "hough_minline": 40,
            "hough_maxgap": 5,
        }

    def cam_setup(self):
        self.res = (640, 480)  # (1024, 768)
        self.cam.resolution = self.res
        self.cam.framerate = 24
        self.sleep(2)  # warmup

    def grab_frame(self):
        out = np.empty((self.res[1], self.res[0], 3), dtype=np.uint8)
        return self.cam.capture(output, "rgb")
        # maybe BGR because opencv? probably not an issue for lanes

    def mask_trap(self, img):
        """
        Mask a trapezoid in the image.
        TODO: less hardcoding
        """
        height, width = img.shape
        trap = np.array(
            [
                [0, height],
                [int(width / 5), int(3 * height / 5)],
                [int(4 * width / 5), int(3 * height / 5)],
                [width, height],
            ]
        )
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, trap, 255)
        return cv2.bitwise_and(img, mask)

    def find_lines(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.GaussianBlur(image, self.config["blur_size"], 0)
        edges = cv2.Canny(img, self.config["thresh_low"], self.config["thresh_high"])
        edges = mask_trap(edges)

        lines = cv2.HoughLinesP(
            edges,
            rho=self.config["hough_rho"],
            theta=self.config["hough_theta"],
            threshold=self.config["hough_thresh"],
            minLineLength=self.config["hough_minline"],
            maxLineGap=self.config["hough_maxgap"],
        )

    """
    Combine lines to averages, find where these intersect base of image,
    and then generate an offset (as % of width) from the mid of the lane
    to the mid of the frame. Left of center is positive.
    """

    def interpret_lines(self, lines):
        # Given line in mx+b form, return a segment that
        # goes from bottom of image to 2/5 up from bottom
        def make_segment(img, line):
            if np.isnan(avg).any():
                return (0, 0), (0, 0)

            y1 = img.shape[0]
            y2 = int(y1 * (3 / 5))

            slope, b = avg
            x1 = int((y1 - b) / slope)
            x2 = int((y2 - b) / slope)

            return (x1, y1), (x2, y2)

        # Combine lines into one line on left and one on right
        # of image
        def average(img, lines):
            left = []
            right = []

            for line in lines:
                x1, x2, y1, y2 = line

                # Get mx+b
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                y_int = parameters[1]

                if slope < 0:
                    left.append((slope, y_int))
                else:
                    right.append((slope, y_int))

            left_avg = np.average(np.array(left), axis=0)
            right_avg = np.average(np.array(right), axis=0)

            left_line = make_segment(img, left_avg)
            right_line = make_segment(img, right_avg)

        # Average lines and find where they intersect base of frame
        left_line, right_line = average(img, lines)
        left_pt = left_line[0][0]
        right_pt = right_line[0][0]

        # Find offset between center of lane & center of frame
        mid_pt = right_pt - left_pt
        width = img_shape[1]
        offset = width - mid_pt
        return offset / width

    def detect_lane(self):
        img = self.grab_frame
        lines = self.find_lines(img)
        offset = self.interpret_lines(lines)
        return offset
