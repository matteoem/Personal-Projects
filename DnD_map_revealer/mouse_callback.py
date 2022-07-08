import copy
import cv2
import config

def mouse_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        if not config.drawing_R:
            config.history.append((copy.deepcopy(config.master_data),copy.deepcopy(config.player_data)))
            config.drawing_L=True
            config.master_data.clear_pixels()
            config.master_data.add_pixels(x,y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if config.drawing_L:
            cv2.line(config.master_data.masked_image,pt1=config.master_data.points[-1],pt2=(x,y),color=config.white,thickness=3)
            config.master_data.add_pixels(x,y)
            config.master_data.imshow(config.master_window)

    elif event==cv2.EVENT_LBUTTONUP:
        if config.drawing_L:
            config.drawing_L=False
            config.master_data.apply_mask(config.image)
            config.player_data.apply_mask(config.image,config.master_data.points)
            config.master_data.imshow(config.master_window)
            config.player_data.imshow(config.player_window)


    if event == cv2.EVENT_RBUTTONDOWN:
        if not config.drawing_L:
            config.history.append((copy.deepcopy(config.master_data),copy.deepcopy(config.player_data)))
            config.master_data.copy_image()
            config.drawing_R=True
            config.starting_vertices = (x,y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if config.drawing_R:
            config.master_data.restore_to_copy()
            cv2.rectangle(config.master_data.masked_image,pt1=config.starting_vertices,pt2=(x,y),color=config.white,thickness=1)
            config.master_data.imshow(config.master_window)

    elif event==cv2.EVENT_RBUTTONUP:
        if config.drawing_R:
            ending_vertices = (x,y)
            rectangles_vertices = [config.starting_vertices,(config.starting_vertices[0],ending_vertices[1]),ending_vertices,(ending_vertices[0],config.starting_vertices[1])]
            config.drawing_R=False
            config.master_data.apply_mask(config.image,rectangles_vertices)
            config.player_data.apply_mask(config.image,rectangles_vertices)
            config.player_data.imshow(config.player_window)
            config.master_data.imshow(config.master_window)
