import cv2
import numpy as np



PIXEL_NEIGHBOUR_TYPE_4 = 'PIXEL_NEIGHBOUR_TYPE_4'
PIXEL_NEIGHBOUR_TYPE_8 = 'PIXEL_NEIGHBOUR_TYPE_8'


def get_neighbours_8(x, y):
    """
    Get 8 neighbours of point(x, y)
    """
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), \
            (x - 1, y), (x + 1, y), \
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def get_neighbours_4(x, y):
    return [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]


def get_neighbours(x, y):
    # import config
    neighbour_type = 'PIXEL_NEIGHBOUR_TYPE_8'
    if neighbour_type == PIXEL_NEIGHBOUR_TYPE_4:
        return get_neighbours_4(x, y)
    else:
        return get_neighbours_8(x, y)


def get_neighbours_fn():
    # import config
    neighbour_type = 'PIXEL_NEIGHBOUR_TYPE_8'
    if neighbour_type == PIXEL_NEIGHBOUR_TYPE_4:
        return get_neighbours_4, 4
    else:
        return get_neighbours_8, 8


def is_valid_cord(x, y, w, h):
    """
    Tell whether the 2D coordinate (x, y) is valid or not.
    If valid, it should be on an h x w image
    """
    return x >= 0 and x < w and y >= 0 and y < h;


def decode_image_by_join(pixel_scores, link_scores,
                         pixel_conf_threshold, link_conf_threshold):
    pixel_mask = pixel_scores >= pixel_conf_threshold
    link_mask = link_scores >= link_conf_threshold
    points = list(zip(*np.where(pixel_mask)))
    h, w = np.shape(pixel_mask)
    group_mask = dict.fromkeys(points, -1)

    def find_parent(point):
        return group_mask[point]

    def set_parent(point, parent):
        group_mask[point] = parent

    def is_root(point):
        return find_parent(point) == -1

    def find_root(point):
        root = point
        update_parent = False
        while not is_root(root):
            root = find_parent(root)
            update_parent = True

        # for acceleration of find_root
        if update_parent:
            set_parent(point, root)

        return root

    def join(p1, p2):
        root1 = find_root(p1)
        root2 = find_root(p2)

        if root1 != root2:
            set_parent(root1, root2)

    def get_all():
        root_map = {}

        def get_index(root):
            if root not in root_map:
                root_map[root] = len(root_map) + 1
            return root_map[root]

        mask = np.zeros_like(pixel_mask, dtype=np.int32)
        for point in points:
            point_root = find_root(point)
            bbox_idx = get_index(point_root)
            mask[point] = bbox_idx
        return mask

    # join by link
    for point in points:
        y, x = point
        neighbours = get_neighbours(x, y)
        for n_idx, (nx, ny) in enumerate(neighbours):
            if is_valid_cord(nx, ny, w, h):
                #                 reversed_neighbours = get_neighbours(nx, ny)
                #                 reversed_idx = reversed_neighbours.index((x, y))
                link_value = link_mask[y, x, n_idx]  # and link_mask[ny, nx, reversed_idx]
                pixel_cls = pixel_mask[ny, nx]
                if link_value and pixel_cls:
                    join(point, (ny, nx))

    mask = get_all()
    return mask



def resize(img, size=None, f=None, fx=None, fy=None, interpolation=None):
    """
    size: (w, h)
    """
    if interpolation is None:
        interpolation = cv2.INTER_LINEAR

    h, w = img.shape
    if fx != None and fy != None:
        return cv2.resize(img, None, fx=fx, fy=fy, interpolation=interpolation)

    if size != None:
        size = np.cast['int'](size)
        #         size = (size[1], size[0])
        size = tuple(size)
        return cv2.resize(img, size, interpolation=interpolation)

    return cv2.resize(img, None, fx=f, fy=f, interpolation=interpolation)

def find_contours(mask, method = None):
    if method is None:
        method = cv2.CHAIN_APPROX_SIMPLE
    mask = np.asarray(mask, dtype = np.uint8)
    mask = mask.copy()
    try:
        contours, _ = cv2.findContours(mask, mode = cv2.RETR_CCOMP,
                                   method = method)
    except:
        _, contours, _ = cv2.findContours(mask, mode = cv2.RETR_CCOMP,
                                  method = method)
    return contours

def min_area_rect(cnt):
    """
    Args:
        xs: numpy ndarray with shape=(N,4). N is the number of oriented bboxes. 4 contains [x1, x2, x3, x4]
        ys: numpy ndarray with shape=(N,4), [y1, y2, y3, y4]
            Note that [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] can represent an oriented bbox.
    Return:
        the oriented rects sorrounding the box, in the format:[cx, cy, w, h, theta].
    """
    rect = cv2.minAreaRect(cnt)
    cx, cy = rect[0]
    w, h = rect[1]
    theta = rect[2]
    box = [cx, cy, w, h, theta]
    return box, w * h

def rect_to_xys(rect, image_shape):
    """Convert rect to xys, i.e., eight points
    The `image_shape` is used to to make sure all points return are valid, i.e., within image area
    """
    h, w = image_shape[0:2]

    def get_valid_x(x):
        if x < 0:
            return 0
        if x >= w:
            return w - 1
        return x

    def get_valid_y(y):
        if y < 0:
            return 0
        if y >= h:
            return h - 1
        return y

    rect = ((rect[0], rect[1]), (rect[2], rect[3]), rect[4])
    points = cv2.boxPoints(rect)
    points = np.int0(points)
    for i_xy, (x, y) in enumerate(points):
        x = get_valid_x(x)
        y = get_valid_y(y)
        points[i_xy, :] = [x, y]
    points = np.reshape(points, -1)
    return points

def mask_to_bboxes(mask, image_shape=None, min_area=None,
                   min_height=None, min_aspect_ratio=None):
    # import config
    feed_shape = [720,1280]

    if image_shape is None:
        image_shape = feed_shape

    image_h, image_w = image_shape[0:2]

    if min_area is None:
        min_area = 300

    if min_height is None:
        min_height = 10
    bboxes = []
    max_bbox_idx = mask.max()
    mask = resize(img=mask, size=(image_w, image_h),
                           interpolation=cv2.INTER_NEAREST)

    for bbox_idx in range(1, max_bbox_idx + 1):
        bbox_mask = mask == bbox_idx
        #         if bbox_mask.sum() < 10:
        #             continue
        cnts = find_contours(bbox_mask)
        if len(cnts) == 0:
            continue
        cnt = cnts[0]
        rect, rect_area = min_area_rect(cnt)

        w, h = rect[2:-1]
        if min(w, h) < min_height:
            continue

        if rect_area < min_area:
            continue

        #         if max(w, h) * 1.0 / min(w, h) < 2:
        #             continue
        xys = rect_to_xys(rect, image_shape)
        bboxes.append(xys)

    return bboxes















