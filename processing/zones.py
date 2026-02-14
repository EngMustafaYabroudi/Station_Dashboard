class WaitingZone:
    def __init__(self, roi, frame_w, frame_h):
        xc, yc, w, h = roi
        self.roi = (
            int((xc - w/2) * frame_w),
            int((yc - h/2) * frame_h),
            int((xc + w/2) * frame_w),
            int((yc + h/2) * frame_h)
        )

    def contains(self, x, y):
        x1, y1, x2, y2 = self.roi
        return x1 <= x <= x2 and y1 <= y <= y2