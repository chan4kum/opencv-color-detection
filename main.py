import argparse
import cv2
import numpy as np

WIN = "HSV Controls"


def nothing(_):
    pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--image")
    args = p.parse_args()

    cv2.namedWindow(WIN)
    for name, init, maxv in [("H min", 0, 179), ("H max", 179, 179), ("S min", 0, 255),
                             ("S max", 255, 255), ("V min", 0, 255), ("V max", 255, 255)]:
        cv2.createTrackbar(name, WIN, init, maxv, nothing)

    still = cv2.imread(args.image) if args.image else None
    if args.image and still is None:
        raise SystemExit(f"Could not read {args.image}")
    cap = None if still is not None else cv2.VideoCapture(0)

    while True:
        if still is not None:
            frame = still.copy()
        else:
            ok, frame = cap.read()
            if not ok:
                break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        g = lambda n: cv2.getTrackbarPos(n, WIN)
        lower = np.array([g("H min"), g("S min"), g("V min")])
        upper = np.array([g("H max"), g("S max"), g("V max")])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Original | Mask | Result", np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result]))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    if cap:
        cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
