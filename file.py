import pygame
import copy
import math

colorS = {
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Black": (0, 0, 0),
    "Green": (0, 255, 0),
    # "White": (255, 255, 255),
}

COLOR_INACTIVE = (100, 80, 255)
COLOR_ACTIVE = (100, 200, 255)
COLOR_LIST_INACTIVE = (255, 100, 100)
COLOR_LIST_ACTIVE = (255, 150, 150)

global attribute_dialog, screen_width, screen_height
attribute_dialog = False
screen_width = 1200
screen_height = 1200

# BACKGROUND_color = (173, 216, 230)
BLACK_color = (0, 0, 0)
NAVBAR_BUTTON_TEXT_color = (0, 0, 0)
BACKGROUND_color = (255, 255, 255)
NAVBAR_BUTTON_color = (140, 217, 173)
DIALOG_BOX_color = (220, 220, 220)
APPLY_BUTTON_color_ALT = (0, 128, 0)
APPLY_BUTTON_color = (0, 164, 0)
SHAPE_BORDER_THICKNESS = 5
RECTANGLE_BORDER_RADIUS = 25
SELECT_THICKNESS = 4


class DrawingEditor:

    def __init__(self):
        global attribute_dialog, screen_width, screen_height
        self.pygame = pygame
        self.pygame.init()
        self.width = screen_width
        self.height = screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.pygame.display.set_caption("Drawing Editor")
        self.running = True
        self.drawFlag = 0
        self.dragging = False
        self.select = False
        self.board = []
        self.SelectedRegion = [[0, 0], [0, 0]]
        self.selection = []
        self.fin_selection = []
        self.mov_flag = 0
        self.mov_start = 0
        self.copied = []
        self.copiedmarker = 0
        attribute_dialog = False

    def run(self):
        while self.running:
            self.screen.fill(BACKGROUND_color)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()
            self.render()
            self.update()

    def update(self):
        global attribute_dialog
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.running = False
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                # Addition
                if attribute_dialog:
                    print("Attribute dialog is open")
                    attribute_dialog.handle_event(event)
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.selected_object = self.get_clicked_object(event.pos)
                    if isinstance(self.selected_object, Group) or isinstance(
                        self.selected_object, Shape
                    ):
                        attribute_dialog = AttributeDialog(self.selected_object)
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    # print("SHIFT")
                    self.selected_object = self.get_clicked_object(event.pos)
                    # print(self.selected_object)
                    if isinstance(self.selected_object, Rect):
                        self.selected_object.set_corner_style(
                            "Rounded"
                            if self.selected_object.corner_style == "Square"
                            else "Square"
                        )
                if pygame.key.get_mods() & pygame.KMOD_ALT:
                    # print("ALT")
                    self.selected_object = self.get_clicked_object(event.pos)
                    if isinstance(self.selected_object, Rect) or isinstance(
                        self.selected_object, Line
                    ):
                        # print("instance")
                        current_color = self.selected_object.color
                        # print("cur: ", current_color)
                        color_values = list(colorS.keys())
                        current_color_name = "Red"
                        for x in colorS.keys():
                            if colorS[x] == current_color:
                                current_color_name = x
                                # print("Match: ", current_color_name)
                        cur_index = color_values.index(current_color_name)
                        next_index = (cur_index + 1) % len(colorS)
                        new_color = color_values[next_index]
                        # print(cur_index, next_index, new_color)
                        self.selected_object.set_color(new_color)

                # Kushal
                flag_draw = 0
                if self.DrawLine.collide(self, event.pos):
                    flag_draw = 1
                if self.DrawRect.collide(self, event.pos):
                    flag_draw = 1
                if self.GrpButton.collideGrp(self, event.pos):
                    flag_draw = 1
                if self.UnGrpButton.unGrp(self, event.pos):
                    flag_draw = 1
                if self.UnGrpAllButton.unGrpAll(self, event.pos):
                    flag_draw = 1
                if self.DelButton.delObj(self, event.pos):
                    flag_draw = 1
                if self.ExportButton.expObjTxt(self, event.pos):
                    flag_draw = 1
                if self.ExportXMLButton.expObjXML(self, event.pos):
                    flag_draw = 1
                if self.LoadButton.LoadObjTxt(self,event.pos):
                    flag_draw=1
                if self.CopyButton.copyObj(self, event.pos):
                    flag_draw = 3
                    # self.select=True

                elif self.MoveSelec(event.pos):
                    flag_draw = 2
                    self.copiedmarker = 0
                else:
                    self.copiedmarker = 0
                    self.SelectedRegion = [[0, 0], [0, 0]]
                    self.fin_selection = []
                    self.mov_flag = 0

                if self.drawFlag == 1 and flag_draw == 0:
                    if self.drawType == "Line":
                        line = Line()
                        line.addBoard(self.board)
                    if self.drawType == "Rect":
                        rect = Rect()
                        rect.addBoard(self.board)
                    self.dragging = True
                    self.select = False
                if flag_draw == 1:
                    self.select = False
                # if flag_draw==2:
                #     self.select=True
                if self.drawFlag == 0 and flag_draw == 0:
                    self.select = True
                    self.selection = []
                    self.SelectedRegion[0][0], self.SelectedRegion[0][1] = (
                        pygame.mouse.get_pos()
                    )
                    self.dragging = True
                if self.drawFlag == 0 and flag_draw == 2:
                    print("OKIE")
                    self.select = False
                if self.drawFlag == 0 and flag_draw == 3:
                    self.copiedmarker = 1
                    self.select = False
                    # self.selection=[]
                    # self.SelectedRegion[0][0],self.SelectedRegion[0][1] = pygame.mouse.get_pos()
                    # self.dragging=True

            elif event.type == self.pygame.MOUSEBUTTONUP:
                if self.drawFlag == 1 and self.dragging == True:
                    self.board[-1].dragging = False
                    self.dragging = False
                    self.drawFlag = 0
                elif self.drawFlag == 0 and self.dragging == True:
                    self.dragging = False

                if self.mov_flag == 1:
                    self.mov_flag = 0
                    self.SelectedRegion = [[0, 0], [0, 0]]
                    # self.select=False
                    # self.select=False
                    # print(self.SelectedRegion)

    def render_navbar(self):
        navbar_height = screen_height // 20
        button_width = screen_width // 13
        button_height = navbar_height // 2
        padding = button_width // 2
        margin = padding // 2
        x_position = (screen_width - (button_width * 10 + margin * 9)) // 2

        self.DrawLine = Button(
            self, "Line", (x_position, margin, 0.5*button_width, button_height)
        )
        self.DrawRect = Button(
            self,
            "Rect",
            (x_position + 0.5*button_width + margin, margin, 0.5*button_width, button_height),
        )
        self.GrpButton = Button(
            self,
            "Group",
            (
                x_position + 2 * (0.5*button_width + margin),
                margin,
                0.7*button_width,
                button_height,
            ),
        )
        self.UnGrpButton = Button(
            self,
            "Ungroup",
            (
                x_position + 3 * (0.5*button_width + margin),
                margin,
                2*button_width,
                button_height,
            ),
        )
        self.UnGrpAllButton = Button(
            self,
            "Ungroup All",
            (
                x_position + 4 * (margin) + 3.5*button_width,
                margin,
                2*button_width,
                button_height,
            ),
        )
        self.CopyButton = Button(
            self,
            "Copy",
            (
                x_position + 5 * (margin) + 5.5*button_width,
                margin,
                0.5*button_width,
                button_height,
            ),
        )
        self.DelButton = Button(
            self,
            "Delete",
            (
                x_position + 6 * (button_width + margin),
                margin,
                0.7*button_width,
                button_height,
            ),
        )
        self.ExportButton = Button(
            self,
            "Export Text",
            (
                x_position + 7 * (margin) + 6.5*button_width,
                margin,
                2*button_width,
                button_height,
            ),
        )
        self.ExportXMLButton = Button(
            self,
            "ExportXML",
            (
                x_position + 8 * (button_width + margin) + 0.5*button_width,
                margin,
                2*button_width,
                button_height,
            ),
        )
        self.LoadButton = Button(
            self,
            "Load",
            (
                x_position + 9 * (button_width + margin) + 1.5*button_width,
                margin,
                0.5*button_width,
                button_height,
            ),
        )

    def render(self):
        global attribute_dialog
        self.clock.tick(60)
        self.render_navbar()
        if self.dragging and self.select:
            self.SelectedRegion[1][0], self.SelectedRegion[1][1] = (
                pygame.mouse.get_pos()
            )
        if self.mov_flag == 1:
            maxX = max(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
            minX = min(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
            maxY = max(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
            minY = min(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
            pygame.draw.rect(
                kaooa.screen,
                BLACK_color,
                pygame.Rect(minX, minY, maxX - minX, maxY - minY),
                1,
            )
            if not (self.MoveSelec(pygame.mouse.get_pos())):
                self.mov_flag = 0
        if self.copiedmarker == 1:
            maxX = max(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
            minX = min(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
            maxY = max(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
            minY = min(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
            pygame.draw.rect(
                kaooa.screen,
                BLACK_color,
                pygame.Rect(minX, minY, maxX - minX, maxY - minY),
                1,
            )
        if self.drawFlag == 0 and self.select:
            self.selectingRegion()
            # print(self.SelectedRegion)
        for obj in self.board:
            obj.draw()
            # shape.draw()

        # Addition
        if attribute_dialog:
            attribute_dialog.render(self.screen)
        self.pygame.display.update()

    def selectingRegion(self):
        originalRegion = [[0, 0], [0, 0]]
        originalRegion[0][0] = self.SelectedRegion[0][0]
        originalRegion[0][1] = self.SelectedRegion[0][1]
        originalRegion[1][0] = self.SelectedRegion[1][0]
        originalRegion[1][1] = self.SelectedRegion[1][1]
        maxX = max(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
        minX = min(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
        maxY = max(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
        minY = min(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
        self.SelectedRegion[0][0] = minX
        self.SelectedRegion[1][0] = maxX
        self.SelectedRegion[0][1] = minY
        self.SelectedRegion[1][1] = maxY
        pygame.draw.rect(
            kaooa.screen,
            BLACK_color,
            pygame.Rect(
                self.SelectedRegion[0][0],
                self.SelectedRegion[0][1],
                self.SelectedRegion[1][0] - self.SelectedRegion[0][0],
                self.SelectedRegion[1][1] - self.SelectedRegion[0][1],
            ),
            1,
        )
        for obj in self.board:
            obj.SelectedHighlight(self)
        # print(len(self.selection))
        self.fin_selection = self.selection.copy()
        self.selection = []
        self.SelectedRegion = originalRegion.copy()

    def MoveSelec(self, pos):
        if self.mov_flag == 0:
            print("OOOH")
            self.mov_flag = 1
            self.mov_start = pos
        # if self.mov_flag==1:
        newRegion = [[0, 0], [0, 0]]
        self.SelectedRegion[0][0] -= self.mov_start[0] - pos[0]
        self.SelectedRegion[1][0] -= self.mov_start[0] - pos[0]
        self.SelectedRegion[0][1] -= self.mov_start[1] - pos[1]
        self.SelectedRegion[1][1] -= self.mov_start[1] - pos[1]
        maxX = max(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
        minX = min(self.SelectedRegion[0][0], self.SelectedRegion[1][0])
        maxY = max(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
        minY = min(self.SelectedRegion[0][1], self.SelectedRegion[1][1])
        newRegion[0][0] = minX
        newRegion[1][0] = maxX
        newRegion[0][1] = minY
        newRegion[1][1] = maxY
        print(newRegion)
        if (
            pos[0] < newRegion[0][0]
            or pos[0] > newRegion[1][0]
            or pos[1] < newRegion[0][1]
            or pos[1] > newRegion[1][1]
        ):
            print("KANDA")
            self.mov_flag = 0
            return False
        print("BHAJIYA")
        for obj in self.fin_selection:
            if obj.obj == "Group":
                self.MoveSelecHelper(self.board[self.board.index(obj)], pos)
                for coords in self.board[self.board.index(obj)].coords:
                    coords[0] = coords[0] - (self.mov_start[0] - pos[0])
                    coords[1] = coords[1] - (self.mov_start[1] - pos[1])
            if obj.obj == "Shape":
                temp_ind = self.board.index(obj)
                for coords in self.board[temp_ind].coords:
                    coords[0] = coords[0] - (self.mov_start[0] - pos[0])
                    coords[1] = coords[1] - (self.mov_start[1] - pos[1])
        self.mov_start = pos
        return True

    def MoveSelecHelper(self, obj, pos):
        for obj_temp in obj.Objects:
            if obj_temp.obj == "Group":
                self.MoveSelecHelper(obj.Objects[obj.Objects.index(obj_temp)], pos)
                for coords in obj.Objects[obj.Objects.index(obj_temp)].coords:
                    coords[0] = coords[0] - (self.mov_start[0] - pos[0])
                    coords[1] = coords[1] - (self.mov_start[1] - pos[1])
            else:
                for coords in obj.Objects[obj.Objects.index(obj_temp)].coords:
                    coords[0] = coords[0] - (self.mov_start[0] - pos[0])
                    coords[1] = coords[1] - (self.mov_start[1] - pos[1])
        return True

    # Addition
    def get_clicked_object(self, pos):
        # Iterate through the objects and return the first one that is within the threshold distance
        threshold = 10
        for obj in self.board:
            if isinstance(obj, Group):
                val = obj.group_get_clicked_object(pos, threshold)
                if val != None:
                    return val
            elif obj.is_within_threshold(pos, threshold):
                return obj
        return None


# Addition
class DropDown:
    def __init__(
        self,
        color_menu,
        color_option,
        x,
        y,
        w,
        h,
        font,
        main,
        options,
        parent_x,
        parent_y,
        surface,
    ):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.parent_x = parent_x
        self.parent_y = parent_y
        self.active_option = -1
        self.option_selected = False
        self.surface = surface

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        # print(self.draw_menu)

        if self.draw_menu:
            # print("Drawing menu")
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    surf,
                    self.color_option[1 if i == self.active_option else 0],
                    rect,
                    0,
                )
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            pygame.display.flip()

        if not self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    surf,
                    DIALOG_BOX_color,
                    rect,
                    0,
                )
            pygame.display.flip()

        pygame.display.flip()

    def is_within_bounds(self, mpos):
        check_left = mpos[0] > self.parent_x + self.rect.x
        # print("Check left:", check_left, mpos[0], self.parent_x + self.rect.x)
        check_right = mpos[0] < self.parent_x + self.rect.x + self.rect.width
        # print(
        #     "Check right:",
        #     check_right,
        #     mpos[0],
        #     self.parent_x + self.rect.x + self.rect.width,
        # )
        check_top = mpos[1] > self.parent_y + self.rect.y
        # print("Check top:", check_top, mpos[1], self.parent_y + self.rect.y)
        check_bottom = mpos[1] < self.parent_y + self.rect.y + self.rect.height
        # print(
        #     "Check bottom:",
        #     check_bottom,
        #     mpos[1],
        #     self.parent_y + self.rect.y + self.rect.height,
        # )

        return check_left and check_right and check_top and check_bottom

    def is_within_bounds_options(self, rect_i, mpos):
        check_left = mpos[0] > self.parent_x + rect_i.x
        # print("2 left:", check_left, mpos[0], self.parent_x + rect_i.x)
        check_right = mpos[0] < self.parent_x + rect_i.x + rect_i.width
        # print(
        #     "2 right:",
        #     check_right,
        #     mpos[0],
        #     self.parent_x + rect_i.x + rect_i.width,
        # )
        check_top = mpos[1] > self.parent_y + rect_i.y
        # print("2 top:", check_top, mpos[1], self.parent_y + rect_i.y)
        check_bottom = mpos[1] < self.parent_y + rect_i.y + rect_i.height
        # print(
        #     "2 bottom:",
        #     check_bottom,
        #     mpos[1],
        #     self.parent_y + rect_i.y + rect_i.height,
        # )

        return check_left and check_right and check_top and check_bottom

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        prev_click = 1 if self.menu_active else 0
        self.menu_active = self.is_within_bounds(mpos)

        # print("test:", mpos, self.rect, self.menu_active)

        if not self.menu_active:
            # print("prev click", prev_click)
            if prev_click == 1:
                # Dropdown menu was active
                # print("Menu prev active")
                check_left = mpos[0] > self.parent_x + self.rect.x
                check_right = mpos[0] < self.parent_x + self.rect.x + self.rect.width
                check_top = mpos[1] > self.parent_y + self.rect.y
                check_bottom = (
                    mpos[1]
                    < self.parent_y
                    + (self.rect.y * len(self.options))
                    + self.rect.height
                )
                if check_left and check_right and check_top and check_bottom:
                    # print("Menu active")
                    self.draw_menu = True
                else:
                    # print("Out of bounds")
                    self.draw_menu = False
            else:
                # Dropdown menu was not active
                # print("Menu not active")
                self.draw_menu = False
                return -1

        self.active_option = -1
        # print("Options: ", self.options)
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            # print("Rect:", i, rect, mpos)
            if self.is_within_bounds_options(rect, mpos):
                print("Option selected:", i)
                self.active_option = i
                break

        # if not self.menu_active and self.active_option == -1:
        #     print("Menu not active and no option selected")
        #     self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("Mouse button clicked at:", event.pos)
                print("Menu active:", self.menu_active)
                print("Active option:", self.active_option)
                if self.menu_active:
                    print("Dropdown menu is active")
                    self.draw_menu = True
                elif self.draw_menu and self.active_option >= 0:
                    print("Dropdown option clicked:", self.options[self.active_option])
                    self.draw_menu = False
                    self.draw(self.surface)  # Redraw the dropdown
                    return self.active_option
        return -1


class AttributeDialog:
    def __init__(self, shape):
        # Initialize the dialog box
        self.shape = shape
        self.width = 800 if isinstance(self.shape, Rect) else 400
        self.height = 300
        self.dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.dialog_surface.fill(DIALOG_BOX_color)
        self.current_shape_color = self.shape.color
        self.current_shape_corner_style = (
            self.shape.corner_style if isinstance(self.shape, Rect) else None
        )
        self.font = pygame.font.Font(None, 30)
        self.apply_changes = False

        self.x_coordinate = (screen_width - self.width) // 2
        self.y_coordinate = (screen_height - self.height) // 2

        # print("X coordinate:", self.x_coordinate)
        # print("Y coordinate:", self.y_coordinate)

        # Create dropdowns
        if isinstance(self.shape, Line):
            self.dropdown_color = DropDown(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                100,
                50,
                200,
                50,
                pygame.font.SysFont(None, 30),
                "color",
                list(colorS.keys()),
                self.x_coordinate,
                self.y_coordinate,
                self.dialog_surface,
            )
        elif isinstance(self.shape, Rect):
            self.dropdown_color = DropDown(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                150,
                50,
                200,
                50,
                pygame.font.SysFont(None, 30),
                "color",
                list(colorS.keys()),
                self.x_coordinate,
                self.y_coordinate,
                self.dialog_surface,
            )
            self.dropdown_corner_style = DropDown(
                [COLOR_INACTIVE, COLOR_ACTIVE],
                [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
                450,
                50,
                200,
                50,
                pygame.font.SysFont(None, 30),
                "Corner Style",
                ["Square", "Rounded"],
                self.x_coordinate,
                self.y_coordinate,
                self.dialog_surface,
            )

    def render(self, screen):
        screen.blit(
            self.dialog_surface,
            (
                self.x_coordinate,
                self.y_coordinate,
            ),
        )
        self.dropdown_color.draw(self.dialog_surface)
        if isinstance(self.shape, Rect):
            self.dropdown_corner_style.draw(self.dialog_surface)
        self.draw_apply_button()

    def draw_apply_button(self):
        if isinstance(self.shape, Rect):
            pygame.draw.rect(
                self.dialog_surface,
                APPLY_BUTTON_color,
                pygame.Rect((self.width // 2) - (self.width // 16), 200, 100, 40),
            )
            pygame.draw.rect(
                self.dialog_surface,
                APPLY_BUTTON_color_ALT,
                pygame.Rect((self.width // 2) - (self.width // 16), 200, 100, 40),
                2,
            )
            button_text = self.font.render("Apply", True, (0, 0, 0))
            self.dialog_surface.blit(
                button_text, ((self.width // 2) - (self.width // 26), 210)
            )
        elif isinstance(self.shape, Line):
            pygame.draw.rect(
                self.dialog_surface,
                APPLY_BUTTON_color,
                pygame.Rect((self.width // 2)- (self.width // 7), 0, 100, 40),
            )
            pygame.draw.rect(
                self.dialog_surface,
                APPLY_BUTTON_color_ALT,
                pygame.Rect((self.width // 2)- (self.width // 7), 0, 100, 40),
                2,
            )
            button_text = self.font.render("Apply", True, (0, 0, 0))
            self.dialog_surface.blit(
                button_text, ((self.width // 2) - (self.width // 7), 0)
            )

    def handle_event(self, event):
        global attribute_dialog
        self.dropdown_color.update([event])
        if isinstance(self.shape, Rect):
            self.dropdown_corner_style.update([event])

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check out of bounds
            if (
                mouse_pos[0] < self.x_coordinate
                or mouse_pos[0] > self.x_coordinate + self.width
            ) or (
                mouse_pos[1] < self.y_coordinate
                or mouse_pos[1] > self.y_coordinate + self.height
            ):
                print("Out of bounds")
                attribute_dialog = False
                return

            # Check if the apply button is clicked
            if isinstance(self.shape, Rect):
                if (
                    self.x_coordinate + ((self.width // 2) - (self.width // 16))
                    <= mouse_pos[0]
                    <= self.x_coordinate + ((self.width // 2) - (self.width // 16)) + 100
                    and self.y_coordinate + 200 <= mouse_pos[1] <= self.y_coordinate + 240
                ):
                    print("Apply button clicked")
                    if self.dropdown_color.active_option >= 0:
                        selected_color = colorS[
                            self.dropdown_color.options[self.dropdown_color.active_option]
                        ]
                        if selected_color != self.shape.color:
                            self.shape.set_color(selected_color)
                    if (
                        isinstance(self.shape, Rect)
                        and self.dropdown_corner_style.active_option >= 0
                    ):
                        selected_corner_style = self.dropdown_corner_style.options[
                            self.dropdown_corner_style.active_option
                        ]
                        if selected_corner_style != self.shape.corner_style:
                            self.shape.set_corner_style(selected_corner_style)
                    attribute_dialog = False
                
            if isinstance(self.shape, Line):
                if (
                    self.x_coordinate + ((self.width // 2)- (self.width // 7))
                    <= mouse_pos[0]
                    <= self.x_coordinate + ((self.width // 2)- (self.width // 7)) + 100
                    and self.y_coordinate + 0 <= mouse_pos[1] <= self.y_coordinate + 40
                ):
                    print("Apply button clicked")
                    if self.dropdown_color.active_option >= 0:
                        selected_color = colorS[
                            self.dropdown_color.options[self.dropdown_color.active_option]
                        ]
                        if selected_color != self.shape.color:
                            self.shape.set_color(selected_color)
                    if (
                        isinstance(self.shape, Rect)
                        and self.dropdown_corner_style.active_option >= 0
                    ):
                        selected_corner_style = self.dropdown_corner_style.options[
                            self.dropdown_corner_style.active_option
                        ]
                        if selected_corner_style != self.shape.corner_style:
                            self.shape.set_corner_style(selected_corner_style)
                    attribute_dialog = False

            # Check if the dropdowns are clicked
            if not isinstance(self.shape, Rect):
                print("Line clicked")
                self.dropdown_color.update([event])
            else:
                print("Rect clicked")
                # If shift is pressed, switch corner style
                self.dropdown_color.update([event])
                self.dropdown_corner_style.update([event])

            print("Mouse button clicked at:", event.pos)
            # Put out of bounds check
            # attribute_dialog = False


class Button:
    def __init__(self, DrawingEditor, text, coords):
        self.text = text
        self.button = pygame.draw.rect(
            DrawingEditor.screen, NAVBAR_BUTTON_color, pygame.Rect(coords)
        )

        font = pygame.font.Font(None, 30)
        text = font.render(text, 1, NAVBAR_BUTTON_TEXT_color)
        DrawingEditor.screen.blit(text, (coords[0], coords[1]))

    def collide(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            DrawingEditor.drawFlag = 1
            DrawingEditor.drawType = self.text
            return True

    def collideGrp(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            new_grp = Group()
            for obj in DrawingEditor.fin_selection:
                if obj in DrawingEditor.board:
                    DrawingEditor.board.remove(obj)
                new_grp.Objects.append(obj)
            DrawingEditor.board.append(new_grp)
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            return True

    def unGrp(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            for obj in DrawingEditor.fin_selection:
                if obj.obj == "Group":
                    # print(len(DrawingEditor.board))
                    DrawingEditor.board.remove(obj)
                    for obj1 in obj.Objects:
                        DrawingEditor.board.append(obj1)
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            return True

    def unGrpAll(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            for obj in DrawingEditor.fin_selection:
                if obj.obj == "Group":
                    self.unGrpAll_helper(DrawingEditor, obj)
                    DrawingEditor.board.remove(obj)
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            return True

    def unGrpAll_helper(self, DrawingEditor, obj):
        temp_objs_to_remove = []
        for obj_temp in obj.Objects:
            if obj_temp.obj == "Group":
                self.unGrpAll_helper(DrawingEditor, obj_temp)
            else:
                DrawingEditor.board.append(obj_temp)
        for obj_2 in temp_objs_to_remove:
            obj.Objects.remove(obj_2)
        return True

    def copyObj(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            DrawingEditor.MoveSelec(pos)
            for obj in DrawingEditor.fin_selection:
                copied_obj = copy.deepcopy(obj)
                DrawingEditor.board.append(copied_obj)
            DrawingEditor.select = True
            # DrawingEditor.fin_selection=[]
            # DrawingEditor.SelectedRegion=[[0,0],[0,0]]
            return True

    def delObj(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            for obj in DrawingEditor.fin_selection:
                DrawingEditor.board.remove(obj)
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            return True

    def get_filename(self,DrawingEditor):
        filename = ""
        input_rect = pygame.Rect(500, 500, 200, 32)
        active = False
        text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            filename = text
                            return filename
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            DrawingEditor.screen.fill((0, 0, 0))
            pygame.draw.rect(DrawingEditor.screen, (255, 255, 255), input_rect, 2)
            font = pygame.font.Font(None, 32)
            text_surface = font.render(text, True, (255, 255, 255))
            DrawingEditor.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.display.flip()
    
    def expObjTxt(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            file_name=self.get_filename(DrawingEditor)
            f = open(file_name+".txt", "w")
            # f = open("export.txt", "w")
            for obj in DrawingEditor.board:
                obj.expTxt(f)
            f.close()
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            print("HI")
            return True

    def expObjXML(self, DrawingEditor, pos):
        if self.button.collidepoint(pos):
            file_name=self.get_filename(DrawingEditor)
            f = open(file_name+".xml", "w")
            f.write("<Drawing>\n")
            for obj in DrawingEditor.board:
                obj.expXML(f, 0)
            f.write("</Drawing>")
            f.close()
            DrawingEditor.fin_selection = []
            DrawingEditor.SelectedRegion = [[0, 0], [0, 0]]
            return True
        
    def LoadObjTxt(self,DrawingEditor,pos):
        if self.button.collidepoint(pos):
            file_name=self.get_filename(DrawingEditor)
            f = open(file_name+".txt", "r")
            DrawingEditor.board=[]
            file_line=f.readline()
            while file_line!="":
                self.LoabObjTxtHelper(DrawingEditor,file_line,f)
                file_line=f.readline()
                    
            DrawingEditor.fin_selection=[]
            DrawingEditor.SelectedRegion=[[0,0],[0,0]]
            return True
        
    def LoabObjTxtHelper(self,DrawingEditor2,line,f):
        # print(line)
        line=line.split()
        # print(f"{line[0]}a")
        if (line[0]=="begin"):
            grp=Group()
            # print("HI")
            if isinstance(DrawingEditor2,Group):
                temp_line=f.readline()
                temp_line2=temp_line
                temp_line2=temp_line2.split()
                while (temp_line2[0]!="end"):
                    print("ok",temp_line)
                    self.LoabObjTxtHelper(grp,temp_line,f)
                    temp_line=f.readline()
                    temp_line2=temp_line
                    temp_line2=temp_line2.split()
                DrawingEditor2.Objects.append(grp)
            else:
                temp_line=f.readline()
                temp_line2=temp_line
                temp_line2=temp_line2.split()
                while (temp_line2[0]!="end"):
                    print("ok",temp_line)
                    self.LoabObjTxtHelper(grp,temp_line,f)
                    temp_line=f.readline()
                    temp_line2=temp_line
                    temp_line2=temp_line2.split()
                DrawingEditor2.board.append(grp)
        if (line[0]=="line"):
            line1=Line()
            line1.coords[0][0]=int(line[1])
            line1.coords[0][1]=int(line[2])
            line1.coords[1][0]=int(line[3])
            line1.coords[1][1]=int(line[4])
            if (line[5]=="r"):
                line1.color=(255,0,0)
            if (line[5]=="g"):
                line1.color=(0,255,0)
            if (line[5]=="b"):
                line1.color=(0,0,255)
            if (line[5]=="k"):
                line1.color=(255,255,255)
            if (line[5]=="w"):
                line1.color=(0,0,0)
            print(type(DrawingEditor2))
            if isinstance(DrawingEditor2,Group):
                print("Hi")
                DrawingEditor2.Objects.append(line1)
            else:
                DrawingEditor2.board.append(line1)
        if (line[0]=="rect"):
            rect1=Rect()
            rect1.coords[0][0]=int(line[1])
            rect1.coords[0][1]=int(line[2])
            rect1.coords[1][0]=int(line[3])
            rect1.coords[1][1]=int(line[4])
            if (line[5]=="r"):
                rect1.color=(255,0,0)
            if (line[5]=="g"):
                rect1.color=(0,255,0)
            if (line[5]=="b"):
                rect1.color=(0,0,255)
            if (line[5]=="k"):
                rect1.color=(255,255,255)
            if (line[5]=="w"):
                rect1.color=(0,0,0)
            if (line[6]=="s"):
                rect1.corner_style="Square"
            if (line[6]=="r"):
                rect1.corner_style="Rounded"
            if isinstance(DrawingEditor2,Group):
                DrawingEditor2.Objects.append(rect1)
            else:
                DrawingEditor2.board.append(rect1)


class Shape:
    def __init__(self):
        self.color = (0, 0, 0)
        self.coords = []
        self.obj = "Shape"
        self.dragging=0
        
    def addBoard(self, board):
        board.append(self)
        board[-1].dragging = True
        board[-1].coords[0][0], board[-1].coords[0][1] = pygame.mouse.get_pos()

    def draw(self):
        pass  # Abstract method, to be implemented by subclasses

    def SelectedHighlight(self, DrawingEditor):
        select_flag = 1
        for coords in self.coords:
            if (
                coords[0] > DrawingEditor.SelectedRegion[0][0]
                and coords[0] < DrawingEditor.SelectedRegion[1][0]
                and coords[1] > DrawingEditor.SelectedRegion[0][1]
                and coords[1] < DrawingEditor.SelectedRegion[1][1]
            ):
                pass
            else:
                select_flag = 0
        if select_flag == 1:
            for coords in self.coords:
                pygame.draw.rect(
                    kaooa.screen,
                    BLACK_color,
                    pygame.Rect(coords[0] - 5, coords[1] - 5, 10, 10),
                    SELECT_THICKNESS,
                )
            DrawingEditor.selection.append(self)

    def SelectedHighlightGrp(self, DrawingEditor):
        select_flag = 1
        for coords in self.coords:
            if (
                coords[0] > DrawingEditor.SelectedRegion[0][0]
                and coords[0] < DrawingEditor.SelectedRegion[1][0]
                and coords[1] > DrawingEditor.SelectedRegion[0][1]
                and coords[1] < DrawingEditor.SelectedRegion[1][1]
            ):
                pass
            else:
                select_flag = 0
        if select_flag == 1:
            for coords in self.coords:
                pygame.draw.rect(
                    kaooa.screen,
                    BLACK_color,
                    pygame.Rect(coords[0] - 5, coords[1] - 5, 10, 10),
                    SELECT_THICKNESS,
                )
            # DrawingEditor.selection.append(self)

    def expTxt(self, f):
        pass

    def expXML(self, f, depth):
        pass


class Line(Shape):
    def __init__(self):
        super().__init__()
        self.coords.append([0, 0])
        self.coords.append([0, 0])
        # Addition
        self.color = (0, 0, 0)

    def draw(self):
        if self.dragging:
            self.coords[1][0], self.coords[1][1] = pygame.mouse.get_pos()
        pygame.draw.line(
            kaooa.screen,
            self.color,
            (self.coords[0][0], self.coords[0][1]),
            (self.coords[1][0], self.coords[1][1]),
            SHAPE_BORDER_THICKNESS,
        )

    def expTxt(self, f):
        f.write("line ")
        f.write(
            str(self.coords[0][0])
            + " "
            + str(self.coords[0][1])
            + " "
            + str(self.coords[1][0])
            + " "
            + str(self.coords[1][1])
            + " "
        )
        if self.color == (255, 0, 0):
            f.write("r\n")
        if self.color == (0, 255, 0):
            f.write("g\n")
        if self.color == (0, 0, 255):
            f.write("b\n")
        if self.color == (255, 255, 255):
            f.write("k\n")
        if self.color == (0, 0, 0):
            f.write("w\n")

    def expXML(self, f, depth):
        indent = ""
        for i in range(depth):
            indent += " "
        f.write(f"{indent}<line>\n")
        f.write(f"{indent} <begin>\n")
        f.write(f"{indent}  <x>{self.coords[0][0]}</x>\n")
        f.write(f"{indent}  <y>{self.coords[0][1]}</y>\n")
        f.write(f"{indent} </begin>\n")
        f.write(f"{indent} <end>\n")
        f.write(f"{indent}  <x>{self.coords[1][0]}</x>\n")
        f.write(f"{indent}  <y>{self.coords[1][1]}</y>\n")
        f.write(f"{indent} </end>\n")
        temp_color = "black"
        if self.color == (255, 0, 0):
            temp_color = "red"
        if self.color == (0, 255, 0):
            temp_color = "green"
        if self.color == (0, 0, 255):
            temp_color = "blue"
        if self.color == (255, 255, 255):
            temp_color = "white"
        f.write(f"{indent} <color>{temp_color}<color>\n")
        f.write(f"{indent}</line>\n")

    # Addition
    def set_color(self, color):
        self.color = color

    def is_within_threshold(self, pos, threshold):
        # Calculate the distance between the mouse position and the line using point-to-line distance formula
        x1, y1 = self.coords[0]
        x2, y2 = self.coords[1]
        x0, y0 = pos

        # Calculate the numerator and denominator for the distance formula
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        # Calculate the distance
        distance = numerator / denominator

        # Check if the distance is within the threshold
        return distance <= threshold


class Rect(Shape):
    def __init__(self):
        super().__init__()
        self.coords.append([0, 0])
        self.coords.append([0, 0])
        # Addition
        self.corner_style = "Square"
        self.color = (0, 0, 0)

    def draw(self):
        if self.dragging:
            self.coords[1][0], self.coords[1][1] = pygame.mouse.get_pos()
        else:
            temp_coords2=[[0,0],[0,0]]
            temp_coords2[0][0]=min(self.coords[1][0],self.coords[0][0])
            temp_coords2[1][0]=max(self.coords[0][0],self.coords[1][0])
            temp_coords2[0][1]=min(self.coords[1][1],self.coords[0][1])
            temp_coords2[1][1]=max(self.coords[0][1],self.coords[1][1])
            self.coords[1][0]=temp_coords2[1][0]
            self.coords[0][0]=temp_coords2[0][0]
            self.coords[1][1]=temp_coords2[1][1]
            self.coords[0][1]=temp_coords2[0][1]
        temp_coords=[[0,0],[0,0]]
        temp_coords[0][0]=min(self.coords[1][0],self.coords[0][0])
        temp_coords[1][0]=max(self.coords[0][0],self.coords[1][0])
        temp_coords[0][1]=min(self.coords[1][1],self.coords[0][1])
        temp_coords[1][1]=max(self.coords[0][1],self.coords[1][1])
        # self.coords[1][0]=temp_coords[1][0]
        # self.coords[0][0]=temp_coords[0][0]
        # self.coords[1][1]=temp_coords[1][1]
        # self.coords[0][1]=temp_coords[0][1]
        pygame.draw.rect(
            kaooa.screen,
            self.color,
            pygame.Rect(
               temp_coords[0][0],
               temp_coords[0][1],
               temp_coords[1][0] -temp_coords[0][0],
               temp_coords[1][1] -temp_coords[0][1],
            ),
            SHAPE_BORDER_THICKNESS,
            (
                RECTANGLE_BORDER_RADIUS if self.corner_style == "Rounded" else 0
            ),  # Border radius for Rounded rectangle
        )

    def expTxt(self, f):
        f.write("rect ")
        f.write(
            str(self.coords[0][0])
            + " "
            + str(self.coords[0][1])
            + " "
            + str(self.coords[1][0])
            + " "
            + str(self.coords[1][1])
            + " "
        )
        if self.color == (255, 0, 0):
            f.write("r ")
        if self.color == (0, 255, 0):
            f.write("g ")
        if self.color == (0, 0, 255):
            f.write("b ")
        if self.color == (255, 255, 255):
            f.write("k ")
        if self.color == (0, 0, 0):
            f.write("w ")
        if self.corner_style == "Square":
            f.write("s\n")
        else:
            f.write("r\n")

    def expXML(self, f, depth):
        indent = ""
        for i in range(depth):
            indent += " "
        f.write(f"{indent}<rectangle>\n")
        f.write(f"{indent} <upper-left>\n")
        f.write(f"{indent}  <x>{self.coords[0][0]}</x>\n")
        f.write(f"{indent}  <y>{self.coords[0][1]}</y>\n")
        f.write(f"{indent} </upper-left>\n")
        f.write(f"{indent} <lower-right>\n")
        f.write(f"{indent}  <x>{self.coords[1][0]}</x>\n")
        f.write(f"{indent}  <y>{self.coords[1][1]}</y>\n")
        f.write(f"{indent} </lower-right>\n")
        temp_color = "black"
        if self.color == (255, 0, 0):
            temp_color = "red"
        if self.color == (0, 255, 0):
            temp_color = "green"
        if self.color == (0, 0, 255):
            temp_color = "blue"
        if self.color == (255, 255, 255):
            temp_color = "white"
        f.write(f"{indent} <color>{temp_color}<color>\n")
        temp_style = "square"
        if self.corner_style == "Rounded":
            temp_style = "rounded"
        f.write(f"{indent} <corner>{temp_style}<corner>\n")
        f.write(f"{indent}</rectangle>\n")

    def set_color(self, color):
        self.color = color

    def set_corner_style(self, style):
        self.corner_style = style

    def is_within_threshold(self, pos, threshold):
        # Calculate the distance from the mouse position to the nearest edge of the rectangle
        x1, y1 = self.coords[0]
        x2, y2 = self.coords[1]
        x0, y0 = pos

        # Calculate the closest point on the rectangle to the mouse position
        closest_x = max(x1, min(x0, x2))
        closest_y = max(y1, min(y0, y2))

        # Calculate the distance between the mouse position and the closest point on the rectangle
        distance = math.sqrt((x0 - closest_x) ** 2 + (y0 - closest_y) ** 2)

        # Check if the distance is within the threshold
        return distance <= threshold


class Group:
    def __init__(self):
        self.obj = "Group"
        self.Objects = []
        self.coords = [[800, 800], [0, 0]]

    def draw(self):
        for obj in self.Objects:
            obj.draw()
            self.coords[0][0] = min(self.coords[0][0], obj.coords[0][0])
            self.coords[0][1] = min(self.coords[0][1], obj.coords[0][1])
            self.coords[1][0] = max(self.coords[1][0], obj.coords[1][0])
            self.coords[1][1] = max(self.coords[1][1], obj.coords[1][1])

    def SelectedHighlight(self, DrawingEditor):
        # print(self.coords)
        for coords in self.coords:
            if (
                coords[0] > DrawingEditor.SelectedRegion[0][0]
                and coords[0] < DrawingEditor.SelectedRegion[1][0]
                and coords[1] > DrawingEditor.SelectedRegion[0][1]
                and coords[1] < DrawingEditor.SelectedRegion[1][1]
            ):
                # print("HI")
                pass
            else:
                # DrawingEditor.SelectedRegion=originalRegion.copy()
                return
        for obj in self.Objects:
            obj.SelectedHighlightGrp(DrawingEditor)
        DrawingEditor.selection.append(self)

    def SelectedHighlightGrp(self, DrawingEditor):
        # print(self.coords)
        for coords in self.coords:
            if (
                coords[0] > DrawingEditor.SelectedRegion[0][0]
                and coords[0] < DrawingEditor.SelectedRegion[1][0]
                and coords[1] > DrawingEditor.SelectedRegion[0][1]
                and coords[1] < DrawingEditor.SelectedRegion[1][1]
            ):
                # print("HI")
                pass
            else:
                # DrawingEditor.SelectedRegion=originalRegion.copy()
                return
        for obj in self.Objects:
            if obj.obj == "Group":
                obj.SelectedHighlight(DrawingEditor)
            else:
                obj.SelectedHighlightGrp(DrawingEditor)
        # DrawingEditor.selection.append(self)
        # DrawingEditor.SelectedRegion=originalRegion.copy()

    def expTxt(self, f):
        f.write("begin\n")
        for obj in self.Objects:
            obj.expTxt(f)
        f.write("end\n")

    def expXML(self, f, depth):
        indent = ""
        for i in range(depth):
            indent += " "
        f.write(f"{indent}<group>\n")
        for obj in self.Objects:
            obj.expXML(f, depth + 1)
        f.write(f"{indent}</group>\n")

    def group_get_clicked_object(self, pos, threshold):
        for obj in self.Objects:
            if isinstance(obj, Group):
                val = obj.group_get_clicked_object(pos, threshold)
                if val != None:
                    return val
            elif obj.is_within_threshold(pos, threshold):
                return obj
        return None


kaooa = DrawingEditor()

kaooa.run()
