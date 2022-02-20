import os
import random
import sys
from importlib import import_module

import pygame

import card_area
import set_cards
import settings


# 画卡牌上的状态的函数，由更新卡牌蒙板调用
def draw_condition(card):
    (condition_x, condition_y) = card.active_condition_rect.topright
    for (num, condition) in enumerate(card.active_condition):
        if num < card.main_game.settings.card_condition_hnumber:
            active_condition_image = card.active_condition_font.render(
                condition[:card.main_game.settings.card_condition_hnumber], True,
                card.main_game.settings.card_mask_font_color3)
            active_condition_image_rect = active_condition_image.get_rect(
                topright=(condition_x, condition_y + num * card.active_condition_font.get_height()))
            card.card_image_mask.blit(active_condition_image, active_condition_image_rect)
        else:
            break


# 现场印卡的类
class Print_Card:
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_target = None  # 这张卡指向的目标卡牌
        self.card_image = None  # 卡牌的图像
        self.card_name = ""  # 这张卡的名称
        self.card_attribute = ()  # 这张卡片的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ()  # 这张卡片的规则关键词，表示卡片有些什么关键词
        self.rule_mark = ()  # 这张卡片的规则效果标志，表示其有些什么效果
        self.card_type = ""  # 卡牌类型
        self.rule_text = ""  # 规则文字，本卡牌在场时的特殊能力
        self.shadow_text = ""  # 卡牌有暗影效果的话，代表其暗影效果的文字说明
        self.describe_text = ""  # 剧情描述的斜体文字

        self.active_condition = {}  # 这张卡片上的状态
        self.active_condition_rect = pygame.Rect(110, 5, 230, 270)
        self.active_condition_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)

        # 创建这个卡牌上活跃数值的蒙板
        self.card_image_mask = pygame.Surface(self.main_game.settings.original_card_size).convert()
        self.card_image_mask.fill((128, 128, 128))
        self.card_image_mask.set_colorkey((128, 128, 128))
        # END

        self.card_order = [None, 0, 0, None, 0, 0]  # 卡牌执行的步骤，在run_game()中每次只执行一步
        self.order_exception = False  # 表示卡牌动作的例外情况，为True时card_order视为[None,...]
        self.pause_card = None  # 表示本卡牌的动作阻断了哪张卡的动作
        self.pause_card_order = None  # 这个值表示卡片阻断的pause_card的动作循环
        self.copy_information = None  # 复制截获的信息，执行动作后再放出，这样其他卡牌也能收到此信息

    # 更新这张卡牌的蒙板
    def update_mask(self):
        pass

    # 重置卡牌
    def reset_card(self):
        self.card_order = [None, 0, 0, None, 0, 0]
        self.order_exception = False
        self.pause_card = None
        self.pause_card_order = None
        self.copy_information = None

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        pass

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        pass

    # 卡牌侦听
    def card_listening(self):
        if self.card_type == "暗影牌":
            if "暗影牌" in self.active_condition and self.active_condition["暗影牌"][
                0] not in self.main_game.clash_area.card_group or self.main_game.information and \
                    self.main_game.information[1][-6:] == "卡牌将要离场" and self.main_game.information[2] == \
                    self.active_condition["暗影牌"][0]:
                if self.card_target:
                    if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self.card_target)
                    else:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck = [self.card_target]
                self.active_condition["暗影牌"][0].active_condition["分配暗影"].remove(self)
                if not self.active_condition["暗影牌"][0].active_condition["分配暗影"]:
                    self.active_condition["暗影牌"][0].active_condition.pop("分配暗影")
                    self.active_condition["暗影牌"][0].update_mask()
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(
                    self)

    # 卡牌的动作循环
    def run_card_order(self):
        pass


# 任务牌的基类
class Task_Group:
    def __init__(self):
        self.card_order = [None, 0, 0, None, 0, 0]  # 卡牌执行的步骤，在run_game()中每次只执行一步
        self.order_exception = False  # 表示卡牌动作的例外情况，为True时card_order视为[None,...]
        self.pause_card = None  # 表示本卡牌的动作阻断了哪张卡的动作
        self.pause_card_order = None  # 这个值表示卡片阻断的pause_card的动作循环
        self.copy_information = None  # 复制截获的信息，执行动作后再放出，这样其他卡牌也能收到此信息
        # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
        self.active_task_point = self.task_point
        self.active_task_point_rect = pygame.Rect(17, 195, 80, 60)
        self.active_task_point_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_task_point_rect.h)
        self.active_task_point_font.bold = True
        # END
        # 创建这个卡牌上活跃数值的蒙板
        self.card_image_mask = pygame.Surface(
            (self.main_game.settings.original_card_size[1], self.main_game.settings.original_card_size[0])).convert()
        self.card_image_mask.fill((128, 128, 128))
        self.card_image_mask.set_colorkey((128, 128, 128))
        # END

    # 更新这张卡牌的蒙板
    def update_mask(self):
        self.card_image_mask.fill((128, 128, 128))
        if self.task_point != None:
            if self.active_task_point < self.task_point:
                active_task_point_image = self.active_task_point_font.render(str(self.active_task_point), True,
                                                                             self.main_game.settings.card_mask_font_color2)
                active_task_point_image_rect = active_task_point_image.get_rect(
                    center=self.active_task_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_task_point_rect)
                self.card_image_mask.blit(active_task_point_image, active_task_point_image_rect)
            elif self.active_task_point > self.task_point:
                active_task_point_image = self.active_task_point_font.render(str(self.active_task_point), True,
                                                                             self.main_game.settings.card_mask_font_color1)
                active_task_point_image_rect = active_task_point_image.get_rect(
                    center=self.active_task_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_task_point_rect)
                self.card_image_mask.blit(active_task_point_image, active_task_point_image_rect)

    # 卡牌侦听
    def card_listening(self):
        pass

    # 卡牌的动作循环
    def run_card_order(self):
        pass


# 敌军牌的基类
class Enemy_Group:
    def __init__(self):
        self.card_order = [None, 0, 0, None, 0, 0]  # 卡牌执行的步骤，在run_game()中每次只执行一步
        self.order_exception = False  # 表示卡牌动作的例外情况，为True时card_order视为[None,...]
        self.pause_card = None  # 表示本卡牌的动作阻断了哪张卡的动作
        self.pause_card_order = None  # 这个值表示卡片阻断的pause_card的动作循环
        self.copy_information = None  # 复制截获的信息，执行动作后再放出，这样其他卡牌也能收到此信息
        if self.card_type == "敌军":
            # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
            self.active_clash_value = self.clash_value  # 活跃交锋值
            self.active_clash_value_rect = pygame.Rect(47, 26, 75, 45)
            self.active_clash_value_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_clash_value_rect.h)
            self.active_clash_value_font.bold = True

            self.active_threat_force = self.threat_force  # 活跃威胁力
            self.active_threat_force_rect = pygame.Rect(52, 101, 65, 46)
            self.active_threat_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_threat_force_rect.h)
            self.active_threat_force_font.bold = True

            self.active_attack_force = self.attack_force  # 活跃攻击力
            self.active_attack_force_rect = pygame.Rect(52, 149, 65, 46)
            self.active_attack_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_attack_force_rect.h)
            self.active_attack_force_font.bold = True

            self.active_defense_force = self.defense_force  # 活跃防御力
            self.active_defense_force_rect = pygame.Rect(52, 197, 65, 46)
            self.active_defense_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_defense_force_rect.h)
            self.active_defense_force_font.bold = True

            self.active_health_point = self.health_point  # 活跃生命值
            self.active_health_point_rect = pygame.Rect(46, 276, 76, 72)
            self.active_health_point_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_health_point_rect.h)
            self.active_health_point_font.bold = True

            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(136, 6, 284, 333)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
            # END
        elif self.card_type == "地区":
            # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
            self.active_threat_force = self.threat_force  # 活跃威胁力
            self.active_threat_force_rect = pygame.Rect(34, 68, 65, 65)
            self.active_threat_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_threat_force_rect.h)
            self.active_threat_force_font.bold = True

            self.active_task_point = self.task_point  # 活跃任务点
            self.active_task_point_rect = pygame.Rect(26, 285, 73, 60)
            self.active_task_point_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_task_point_rect.h)
            self.active_task_point_font.bold = True

            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(106, 65, 312, 280)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
            # END
        elif self.card_type == "阴谋":
            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(80, 7, 340, 330)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
        elif self.card_type == "目标":
            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(12, 97, 405, 257)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)

        # 创建这个卡牌上活跃数值的蒙板
        self.card_image_mask = pygame.Surface(self.main_game.settings.original_card_size).convert()
        self.card_image_mask.fill((128, 128, 128))
        self.card_image_mask.set_colorkey((128, 128, 128))
        # END

    # 更新这张卡牌的蒙板
    def update_mask(self):
        self.card_image_mask.fill((128, 128, 128))
        if self.card_type == "敌军":
            # 画活跃交锋值
            if self.active_clash_value < self.clash_value:
                active_clash_value_image = self.active_clash_value_font.render(str(self.active_clash_value), True,
                                                                               self.main_game.settings.card_mask_font_color1)
                active_clash_value_image_rect = active_clash_value_image.get_rect(
                    center=self.active_clash_value_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_clash_value_rect)
                self.card_image_mask.blit(active_clash_value_image, active_clash_value_image_rect)
            elif self.active_clash_value > self.clash_value:
                active_clash_value_image = self.active_clash_value_font.render(str(self.active_clash_value), True,
                                                                               self.main_game.settings.card_mask_font_color2)
                active_clash_value_image_rect = active_clash_value_image.get_rect(
                    center=self.active_clash_value_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_clash_value_rect)
                self.card_image_mask.blit(active_clash_value_image, active_clash_value_image_rect)

            # 画活跃威胁力
            if self.active_threat_force < self.threat_force:
                active_threat_force_image = self.active_threat_force_font.render(str(self.active_threat_force), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_threat_force_image_rect = active_threat_force_image.get_rect(
                    center=self.active_threat_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_threat_force_rect)
                self.card_image_mask.blit(active_threat_force_image, active_threat_force_image_rect)
            elif self.active_threat_force > self.threat_force:
                active_threat_force_image = self.active_threat_force_font.render(str(self.active_threat_force), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_threat_force_image_rect = active_threat_force_image.get_rect(
                    center=self.active_threat_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_threat_force_rect)
                self.card_image_mask.blit(active_threat_force_image, active_threat_force_image_rect)

            # 画活跃攻击力
            if self.active_attack_force < self.attack_force:
                active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_attack_force_image_rect = active_attack_force_image.get_rect(
                    center=self.active_attack_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_attack_force_rect)
                self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)
            elif self.active_attack_force > self.attack_force:
                active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_attack_force_image_rect = active_attack_force_image.get_rect(
                    center=self.active_attack_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_attack_force_rect)
                self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)

            # 画活跃防御力
            if self.active_defense_force < self.defense_force:
                active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                                   self.main_game.settings.card_mask_font_color2)
                active_defense_force_image_rect = active_defense_force_image.get_rect(
                    center=self.active_defense_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_defense_force_rect)
                self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)
            elif self.active_defense_force > self.defense_force:
                active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                                   self.main_game.settings.card_mask_font_color1)
                active_defense_force_image_rect = active_defense_force_image.get_rect(
                    center=self.active_defense_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_defense_force_rect)
                self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)

            # 画活跃生命值
            if self.active_health_point < self.health_point:
                active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_health_point_image_rect = active_health_point_image.get_rect(
                    center=self.active_health_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_health_point_rect)
                self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)
            elif self.active_health_point > self.health_point:
                active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_health_point_image_rect = active_health_point_image.get_rect(
                    center=self.active_health_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_health_point_rect)
                self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)
        elif self.card_type == "地区":
            # 画活跃威胁力
            if self.active_threat_force < self.threat_force:
                active_threat_force_image = self.active_threat_force_font.render(str(self.active_threat_force), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_threat_force_image_rect = active_threat_force_image.get_rect(
                    center=self.active_threat_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_threat_force_rect)
                self.card_image_mask.blit(active_threat_force_image, active_threat_force_image_rect)
            elif self.active_threat_force > self.threat_force:
                active_threat_force_image = self.active_threat_force_font.render(str(self.active_threat_force), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_threat_force_image_rect = active_threat_force_image.get_rect(
                    center=self.active_threat_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_threat_force_rect)
                self.card_image_mask.blit(active_threat_force_image, active_threat_force_image_rect)

            # 画活跃任务点
            if self.active_task_point < self.task_point:
                active_task_point_image = self.active_task_point_font.render(str(self.active_task_point),
                                                                             True,
                                                                             self.main_game.settings.card_mask_font_color2)
                active_task_point_image_rect = active_task_point_image.get_rect(
                    center=self.active_task_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_task_point_rect)
                self.card_image_mask.blit(active_task_point_image, active_task_point_image_rect)
            elif self.active_task_point > self.task_point:
                active_task_point_image = self.active_task_point_font.render(str(self.active_task_point),
                                                                             True,
                                                                             self.main_game.settings.card_mask_font_color1)
                active_task_point_image_rect = active_task_point_image.get_rect(
                    center=self.active_task_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_task_point_rect)
                self.card_image_mask.blit(active_task_point_image, active_task_point_image_rect)

        # 画卡牌状态
        draw_condition(self)

    # 重置卡牌
    def reset_card(self):
        self.card_order = [None, 0, 0, None, 0, 0]
        self.order_exception = False
        self.pause_card = None
        self.pause_card_order = None
        self.copy_information = None
        if self.card_type == "敌军":
            self.active_clash_value = self.clash_value  # 重置活跃交锋值
            self.active_threat_force = self.threat_force  # 重置活跃威胁力
            self.active_attack_force = self.attack_force  # 重置活跃攻击力
            self.active_defense_force = self.defense_force  # 重置活跃防御力
            self.active_health_point = self.health_point  # 重置活跃生命值
        elif self.card_type == "地区":
            self.active_threat_force = self.threat_force  # 重置活跃威胁力
            self.active_task_point = self.task_point  # 重置活跃任务点
        self.active_condition = {}  # 重置这张卡片上的状态

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        button_1 = []
        for condition in self.active_condition:
            if self.active_condition[condition]:
                button_1_X = []
                for target in self.active_condition[condition]:
                    button_1_X.append((str(target), None))
            else:
                button_1_X = None
            button_1.append((condition, button_1_X))
        button_2 = []
        if self.card_type == "敌军":
            button_2.append(("交锋值:" + str(self.active_clash_value), None))
            button_2.append(("威胁力:" + str(self.active_threat_force), None))
            button_2.append(("攻击力:" + str(self.active_attack_force), None))
            button_2.append(("防御力:" + str(self.active_defense_force), None))
            button_2.append(("生命值:" + str(self.active_health_point), None))
        elif self.card_type == "地区":
            button_2.append(("威胁力:" + str(self.active_threat_force), None))
            button_2.append(("探索点:" + str(self.active_task_point), None))
        button = [("查看状态", button_1), ("查看属性", button_2)]
        if not self.main_game.task_area.region_card and self.card_type == "地区" and self.main_game.threat_area.current_phase == 3 and self in self.main_game.scenario_area.card_group:
            button.insert(0, ("探索", None))
        elif self.main_game.threat_area.current_phase == 4 and self.main_game.threat_area.current_step == 0 and self.card_type == "敌军" and self in self.main_game.scenario_area.card_group:
            button.insert(0, ("交锋", None))
        elif self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4 and not self.main_game.threat_area.action_window and self in self.main_game.clash_area.card_group and not hasattr(
                self.main_game.threat_area,
                "enemy") and "防御中" not in self.active_condition and "已防御" not in self.active_condition:
            button.insert(0, ("选为攻击目标", None))
        elif self.main_game.threat_area.action_window and "行动" in self.rule_mark and self.main_game.on_spot(
                self) and "已横置" not in self.active_condition and "行动后" not in self.active_condition and "暗影牌" not in self.active_condition and self.card_type != "目标":
            button.insert(0, ("行动", None))
        self.main_game.button_option.import_button(self, button)

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        if self.main_game.button_option.option // 100000:
            for (num, button) in enumerate(self.main_game.button_option.buttons):
                if button[0] == "探索" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["探索", 0, 0, False, 0, 0]
                elif button[0] == "交锋" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["交锋", 0, 0, False, 0, 0]
                elif button[0] == "选为攻击目标" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["选为攻击目标", 0, 0, False, 0, 0]
                elif button[0] == "行动" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["行动", 0, 0, False, 0, 0]
            self.main_game.button_option.reset()
            self.main_game.select_card = None

    # 卡牌侦听
    def card_listening(self):
        if self.card_type == "敌军" and not self.active_health_point:
            self.active_health_point = -1
            self.card_order = ["被消灭", 0, 0, False, 0, 0]
        elif self.card_type == "地区" and not self.active_task_point:
            self.active_task_point = -1
            self.card_order = ["已探索", 0, 0, False, 0, 0]
        elif "暗影牌" in self.active_condition and self.active_condition["暗影牌"][
            0] not in self.main_game.clash_area.card_group and "分配暗影" in self.active_condition["暗影牌"][
            0].active_condition and self in self.active_condition["暗影牌"][0].active_condition["分配暗影"]:
            if "暗影" in self.rule_mark:
                self.card_order = ["弃除暗影", 0, 0, False, 0, 0]
            else:
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = [self]
                self.main_game.card_estimate(self.active_condition["暗影牌"][0])[self.active_condition["暗影牌"][0]].remove(
                    self)
            self.active_condition["暗影牌"][0].active_condition["分配暗影"].remove(self)
            if not self.active_condition["暗影牌"][0].active_condition["分配暗影"]:
                self.active_condition["暗影牌"][0].active_condition.pop("分配暗影")
                self.active_condition["暗影牌"][0].update_mask()

    # 卡牌的动作循环
    def run_card_order(self):
        if self.card_order[0] == "探索" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
            elif not self.main_game.information:
                if not self.main_game.task_area.region_card:
                    self.main_game.information = [0, "地区卡牌将要激活", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "探索" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if not self.main_game.task_area.region_card:
                    self.main_game.task_area.region_card[self] = self.main_game.scenario_area.card_group.pop(self)
                    self.main_game.information = [0, "地区卡牌激活后", self]
                    self.main_game.threat_area.order[1] += 1
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "交锋" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要交锋", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "交锋" and self.card_order[1] == 1:
            if self.card_order[2]:
                if self.main_game.threat_area.current_phase == 4 and self.main_game.threat_area.current_step == 0:
                    self.main_game.threat_area.order[1] += 1
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.clash_area.card_group[self] = self.main_game.scenario_area.card_group.pop(self)
                self.main_game.information = [0, "敌军卡牌交锋后", self]
                if self.main_game.threat_area.current_phase == 4 and self.main_game.threat_area.current_step == 0:
                    self.main_game.threat_area.order[1] += 1
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "选为攻击目标" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要选为攻击目标", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "选为攻击目标" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4:
                    self.main_game.threat_area.enemy = self
                self.active_condition["防御中"] = []
                self.update_mask()
                self.main_game.information = [0, "敌军卡牌选为攻击目标后", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "选为攻击目标" and self.card_order[1] == 2:
            self.order_exception = True
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information and self.main_game.next_step:
                self.main_game.next_step = 0
                if self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4:
                    if self.active_condition["防御中"]:
                        self.main_game.information = [0, "将要离开宣告攻击目标步骤", "order"]
                        self.main_game.threat_area.order[4] += 1
                    else:
                        del self.main_game.threat_area.enemy
                        self.main_game.threat_area.order[4] = 0
                if not self.active_condition["防御中"]:
                    self.active_condition.pop("防御中")
                    self.update_mask()
                self.order_exception = False
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌将要被消灭", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "敌军卡牌被消灭后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, self.card_type + "卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, self.card_type + "卡牌被弃除后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "已探索" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "地区卡牌将要已探索", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "已探索" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "地区卡牌已探索后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "离场" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌将要离场", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "离场" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                our_affiliate = []
                enemy_affiliate = []
                target_affiliate = []
                if self.main_game.card_estimate(self)[self]:
                    for card in self.main_game.card_estimate(self)[self]:
                        if card.card_order[0]:
                            return
                        if card.card_type == "目标":
                            target_affiliate.append(card)
                        elif self.main_game.player_control(card):
                            our_affiliate.append(card)
                        else:
                            enemy_affiliate.append(card)
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌离场后", self]
                self.main_game.card_estimate(self).pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    for card in our_affiliate:
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = our_affiliate
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in enemy_affiliate:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
                    if self.card_order[-1] == "弃牌堆":
                        if self.victory_points:
                            if self.main_game.threat_area.victory_point_deck:
                                self.main_game.threat_area.victory_point_deck.insert(0, self)
                            else:
                                self.main_game.threat_area.victory_point_deck = [self]
                        else:
                            self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, self)
                else:
                    if self.victory_points:
                        if self.card_order[-1] == "弃牌堆":
                            if self.main_game.threat_area.victory_point_deck:
                                self.main_game.threat_area.victory_point_deck.insert(0, self)
                            else:
                                self.main_game.threat_area.victory_point_deck = [self]
                        self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
                    else:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck = []
                        if self.card_order[-1] == "弃牌堆":
                            self.main_game.encounterdiscard_area.encounterdiscard_deck.append(self)
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.extend(enemy_affiliate)
                for target in target_affiliate:
                    target.reset_card()
                    target.update_mask()
                    self.main_game.scenario_area.card_group[target] = None
                if self.card_order[-1] == "遭遇附属区":
                    pass
                elif self.card_order[-1] == "牌组顶端":
                    self.reset_card()
                    self.update_mask()
                    if self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.insert(0, self)
                    else:
                        self.main_game.encounter_area.encounter_deck = [self]
                elif self.card_order[-1] == "洗回牌组":
                    self.reset_card()
                    self.update_mask()
                    if self.main_game.encounter_area.encounter_deck:
                        self.main_game.encounter_area.encounter_deck.insert(0, self)
                        random.shuffle(self.main_game.encounter_area.encounter_deck)
                    else:
                        self.main_game.encounter_area.encounter_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]


# 英雄牌的基类
class Hero_Group:
    def __init__(self):
        self.card_order = [None, 0, 0, None, 0, 0]  # 卡牌执行的步骤，在run_game()中每次只执行一步
        self.order_exception = False  # 表示卡牌动作的例外情况，为True时card_order视为[None,...]
        self.pause_card = None  # 表示本卡牌的动作阻断了哪张卡的动作
        self.pause_card_order = None  # 这个值表示卡片阻断的pause_card的动作循环
        self.copy_information = None  # 复制截获的信息，执行动作后再放出，这样其他卡牌也能收到此信息
        # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
        self.active_threat = self.initial_threat  # 活跃威胁值
        self.active_threat_rect = pygame.Rect(48, 23, 78, 50)
        self.active_threat_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_threat_rect.h)
        self.active_threat_font.bold = True

        self.active_willpower = self.willpower  # 活跃意志力
        self.active_willpower_rect = pygame.Rect(54, 98, 65, 45)
        self.active_willpower_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_willpower_rect.h)
        self.active_willpower_font.bold = True

        self.active_attack_force = self.attack_force  # 活跃攻击力
        self.active_attack_force_rect = pygame.Rect(54, 146, 65, 45)
        self.active_attack_force_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_attack_force_rect.h)
        self.active_attack_force_font.bold = True

        self.active_defense_force = self.defense_force  # 活跃防御力
        self.active_defense_force_rect = pygame.Rect(54, 194, 65, 45)
        self.active_defense_force_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_defense_force_rect.h)
        self.active_defense_force_font.bold = True

        self.active_health_point = self.health_point  # 活跃生命值
        self.active_health_point_rect = pygame.Rect(47, 274, 75, 70)
        self.active_health_point_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_health_point_rect.h)
        self.active_health_point_font.bold = True

        self.active_resource = 0  # 英雄资源池中的资源点数
        self.active_resource_rect = pygame.Rect(328, 506, 70, 70)
        self.active_resource_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_resource_rect.h)

        self.active_condition = {}  # 这张卡片上的状态
        self.active_condition_rect = pygame.Rect(136, 6, 284, 340)
        self.active_condition_font = pygame.font.Font(
            os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
            self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
        # END
        # 创建这个卡牌上活跃数值的蒙板
        self.card_image_mask = pygame.Surface(self.main_game.settings.original_card_size).convert()
        self.card_image_mask.fill((128, 128, 128))
        self.card_image_mask.set_colorkey((128, 128, 128))
        # END

    # 更新这张卡牌的蒙板
    def update_mask(self):
        self.card_image_mask.fill((128, 128, 128))
        # 画活跃威胁值
        if self.active_threat < self.initial_threat:
            active_threat_image = self.active_threat_font.render(str(self.active_threat), True,
                                                                 self.main_game.settings.card_mask_font_color2)
            active_threat_image_rect = active_threat_image.get_rect(center=self.active_threat_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_threat_rect)
            self.card_image_mask.blit(active_threat_image, active_threat_image_rect)
        elif self.active_threat > self.initial_threat:
            active_threat_image = self.active_threat_font.render(str(self.active_threat), True,
                                                                 self.main_game.settings.card_mask_font_color1)
            active_threat_image_rect = active_threat_image.get_rect(center=self.active_threat_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_threat_rect)
            self.card_image_mask.blit(active_threat_image, active_threat_image_rect)

        # 画活跃意志力
        if self.active_willpower < self.willpower:
            active_willpower_image = self.active_willpower_font.render(str(self.active_willpower), True,
                                                                       self.main_game.settings.card_mask_font_color1)
            active_willpower_image_rect = active_willpower_image.get_rect(center=self.active_willpower_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_willpower_rect)
            self.card_image_mask.blit(active_willpower_image, active_willpower_image_rect)
        elif self.active_willpower > self.willpower:
            active_willpower_image = self.active_willpower_font.render(str(self.active_willpower), True,
                                                                       self.main_game.settings.card_mask_font_color2)
            active_willpower_image_rect = active_willpower_image.get_rect(center=self.active_willpower_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_willpower_rect)
            self.card_image_mask.blit(active_willpower_image, active_willpower_image_rect)

        # 画活跃攻击力
        if self.active_attack_force < self.attack_force:
            active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                             self.main_game.settings.card_mask_font_color1)
            active_attack_force_image_rect = active_attack_force_image.get_rect(
                center=self.active_attack_force_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_attack_force_rect)
            self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)
        elif self.active_attack_force > self.attack_force:
            active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                             self.main_game.settings.card_mask_font_color2)
            active_attack_force_image_rect = active_attack_force_image.get_rect(
                center=self.active_attack_force_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_attack_force_rect)
            self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)

        # 画活跃防御力
        if self.active_defense_force < self.defense_force:
            active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                               self.main_game.settings.card_mask_font_color1)
            active_defense_force_image_rect = active_defense_force_image.get_rect(
                center=self.active_defense_force_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_defense_force_rect)
            self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)
        elif self.active_defense_force > self.defense_force:
            active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                               self.main_game.settings.card_mask_font_color2)
            active_defense_force_image_rect = active_defense_force_image.get_rect(
                center=self.active_defense_force_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_defense_force_rect)
            self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)

        # 画活跃生命值
        if self.active_health_point < self.health_point:
            active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                             self.main_game.settings.card_mask_font_color1)
            active_health_point_image_rect = active_health_point_image.get_rect(
                center=self.active_health_point_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_health_point_rect)
            self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)
        elif self.active_health_point > self.health_point:
            active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                             self.main_game.settings.card_mask_font_color2)
            active_health_point_image_rect = active_health_point_image.get_rect(
                center=self.active_health_point_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_health_point_rect)
            self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)

        # 画资源点数
        if self.active_resource > 0:
            active_resource_image = self.active_resource_font.render(str(self.active_resource), True,
                                                                     self.main_game.settings.card_mask_font_color3)
            active_resource_image_rect = active_resource_image.get_rect(
                center=self.active_resource_rect.center)
            resource_image = pygame.transform.scale(self.main_game.resource_image,
                                                    self.active_resource_rect.size).convert()
            resource_image.set_colorkey((0, 0, 0))
            self.card_image_mask.blit(resource_image, self.active_resource_rect)
            self.card_image_mask.blit(active_resource_image, active_resource_image_rect)

        # 画卡牌状态
        draw_condition(self)

    # 重置卡牌
    def reset_card(self):
        self.card_order = [None, 0, 0, None, 0, 0]
        self.order_exception = False
        self.pause_card = None
        self.pause_card_order = None
        self.copy_information = None
        self.active_threat = self.initial_threat  # 重置活跃威胁值
        self.active_willpower = self.willpower  # 重置活跃意志力
        self.active_attack_force = self.attack_force  # 重置活跃攻击力
        self.active_defense_force = self.defense_force  # 重置活跃防御力
        self.active_health_point = self.health_point  # 重置活跃生命值
        self.active_resource = 0  # 重置英雄资源池中的资源点数
        self.active_condition = {}  # 重置这张卡片上的状态

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        button_1 = []
        for condition in self.active_condition:
            if self.active_condition[condition]:
                button_1_X = []
                for target in self.active_condition[condition]:
                    button_1_X.append((str(target), None))
            else:
                button_1_X = None
            button_1.append((condition, button_1_X))
        button_2 = [("威胁值:" + str(self.active_threat), None)]
        button_2.append(("意志力:" + str(self.active_willpower), None))
        button_2.append(("攻击力:" + str(self.active_attack_force), None))
        button_2.append(("防御力:" + str(self.active_defense_force), None))
        button_2.append(("生命值:" + str(self.active_health_point), None))
        button_2.append(("资源点:" + str(self.active_resource), None))
        button = [("查看状态", button_1), ("查看属性", button_2)]
        if self.main_game.threat_area.current_phase == 2 and self.main_game.threat_area.current_step == 0 and not self.main_game.threat_area.action_window and self in self.main_game.role_area.card_group and "已横置" not in self.active_condition and "任务中" not in self.active_condition:
            button.insert(0, ("指派", None))
        elif self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 1 and not self.main_game.threat_area.action_window and self in self.main_game.role_area.card_group and "宣告防御" not in self.active_condition and "已横置" not in self.active_condition:
            button.insert(0, ("宣告防御", None))
        elif self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4 and not self.main_game.threat_area.action_window and self in self.main_game.role_area.card_group and "宣告攻击" not in self.active_condition and "已横置" not in self.active_condition and hasattr(
                self.main_game.threat_area, "enemy") and self.main_game.threat_area.enemy:
            button.insert(0, ("宣告攻击", None))
        elif self.main_game.threat_area.action_window and "行动" in self.rule_mark and self.main_game.on_spot(
                self) and "已横置" not in self.active_condition and "行动后" not in self.active_condition and "暗影牌" not in self.active_condition:
            button.insert(0, ("行动", None))
        self.main_game.button_option.import_button(self, button)

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        if self.main_game.button_option.option // 100000:
            for (num, button) in enumerate(self.main_game.button_option.buttons):
                if button[0] == "指派" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["指派", 0, 0, False, 0, 0]
                elif button[0] == "宣告防御" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["宣告防御", 0, 0, False, 0, 0]
                elif button[0] == "宣告攻击" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["宣告攻击", 0, 0, False, 0, 0]
                elif button[0] == "行动" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["行动", 0, 0, False, 0, 0]
            self.main_game.button_option.reset()
            self.main_game.select_card = None

    # 卡牌侦听
    def card_listening(self):
        if not self.active_health_point:
            self.active_health_point = -1
            self.card_order = ["被消灭", 0, 0, False, 0, 0]

    # 卡牌的动作循环
    def run_card_order(self):
        if self.card_order[0] == "指派" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要执行任务", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_condition["任务中"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌执行任务后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要宣告防御", self, self.main_game.threat_area.enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.enemy.active_condition["攻击中"].append(self)
                self.active_condition["宣告防御"] = [self.main_game.threat_area.enemy]
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌宣告防御后", self, self.main_game.threat_area.enemy]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要宣告攻击", self, self.main_game.threat_area.enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.enemy.active_condition["防御中"].append(self)
                self.active_condition["宣告攻击"] = [self.main_game.threat_area.enemy]
                self.update_mask()
                self.main_game.information = [0, "英雄卡牌宣告攻击后", self, self.main_game.threat_area.enemy]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要被消灭", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌被消灭后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "英雄卡牌被弃除后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "离场" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌将要离场", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "离场" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                our_affiliate = []
                enemy_affiliate = []
                target_affiliate = []
                if self.main_game.card_estimate(self)[self]:
                    for card in self.main_game.card_estimate(self)[self]:
                        if card.card_order[0]:
                            return
                        if card.card_type == "目标":
                            target_affiliate.append(card)
                        elif self.main_game.player_control(card):
                            our_affiliate.append(card)
                        else:
                            enemy_affiliate.append(card)
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌离场后", self]
                self.main_game.card_estimate(self).pop(self)
                self.main_game.role_area.hero_group.remove(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    for card in our_affiliate:
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                    if self.card_order[-1] == "弃牌堆":
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = []
                    if self.card_order[-1] == "弃牌堆":
                        self.main_game.playerdiscard_area.playerdiscard_deck.append(self)
                    self.main_game.playerdiscard_area.playerdiscard_deck.extend(our_affiliate)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in enemy_affiliate:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
                for target in target_affiliate:
                    target.reset_card()
                    target.update_mask()
                    self.main_game.scenario_area.card_group[target] = None
                if self.card_order[-1] == "遭遇附属区":
                    self.active_condition = {"囚犯": None}
                    self.update_mask()
                    if self.main_game.encounter_area.encounter_affiliated:
                        self.main_game.encounter_area.encounter_affiliated.append(self)
                    else:
                        self.main_game.encounter_area.encounter_affiliated = [self]
                self.card_order = [None, 0, 0, None, 0, 0]


# 玩家牌的基类
class Player_Group:
    def __init__(self):
        self.card_order = [None, 0, 0, None, 0, 0]  # 卡牌执行的步骤，在run_game()中每次只执行一步
        self.order_exception = False  # 表示卡牌动作的例外情况，为True时card_order视为[None,...]
        self.pause_card = None  # 表示本卡牌的动作阻断了哪张卡的动作
        self.pause_card_order = None  # 这个值表示卡片阻断的pause_card的动作循环
        self.copy_information = None  # 复制截获的信息，执行动作后再放出，这样其他卡牌也能收到此信息
        if self.card_type == "盟友":
            # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
            self.active_card_cost = self.card_cost  # 活跃卡牌费用
            self.active_card_cost_rect = pygame.Rect(52, 15, 70, 70)
            self.active_card_cost_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_card_cost_rect.h)
            self.active_card_cost_font.bold = True

            self.active_willpower = self.willpower  # 活跃意志力
            self.active_willpower_rect = pygame.Rect(54, 102, 65, 45)
            self.active_willpower_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_willpower_rect.h)
            self.active_willpower_font.bold = True

            self.active_attack_force = self.attack_force  # 活跃攻击力
            self.active_attack_force_rect = pygame.Rect(54, 150, 65, 45)
            self.active_attack_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_attack_force_rect.h)
            self.active_attack_force_font.bold = True

            self.active_defense_force = self.defense_force  # 活跃防御力
            self.active_defense_force_rect = pygame.Rect(54, 198, 65, 45)
            self.active_defense_force_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_defense_force_rect.h)
            self.active_defense_force_font.bold = True

            self.active_health_point = self.health_point  # 活跃生命值
            self.active_health_point_rect = pygame.Rect(47, 274, 75, 70)
            self.active_health_point_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_health_point_rect.h)
            self.active_health_point_font.bold = True

            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(136, 6, 284, 334)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
            # END
        elif self.card_type == "附属":
            # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
            self.active_card_cost = self.card_cost  # 活跃卡牌费用
            self.active_card_cost_rect = pygame.Rect(24, 26, 60, 60)
            self.active_card_cost_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_card_cost_rect.h)
            self.active_card_cost_font.bold = True

            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(90, 60, 290, 280)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
            # END
        elif self.card_type == "事件":
            # 这个卡牌上所有活跃(会变化)的数值及其相对于settings里原始卡牌图像大小的位置信息
            self.active_card_cost = self.card_cost  # 活跃卡牌费用
            self.active_card_cost_rect = pygame.Rect(24, 10, 66, 60)
            self.active_card_cost_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_card_cost_rect.h)
            self.active_card_cost_font.bold = True

            self.active_condition = {}  # 这张卡片上的状态
            self.active_condition_rect = pygame.Rect(100, 7, 320, 335)
            self.active_condition_font = pygame.font.Font(
                os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                self.active_condition_rect.h // self.main_game.settings.card_condition_hnumber)
            # END

        # 创建这个卡牌上活跃数值的蒙板
        self.card_image_mask = pygame.Surface(self.main_game.settings.original_card_size).convert()
        self.card_image_mask.fill((128, 128, 128))
        self.card_image_mask.set_colorkey((128, 128, 128))

    # 更新这张卡牌的蒙板
    def update_mask(self):
        self.card_image_mask.fill((128, 128, 128))
        # 画活跃卡牌费用
        if type(self.card_cost) != int:
            if self.active_card_cost != self.card_cost:
                active_card_cost_image = self.active_card_cost_font.render(str(self.active_card_cost), True,
                                                                           self.main_game.settings.font_color)
                active_card_cost_image_rect = active_card_cost_image.get_rect(center=self.active_card_cost_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_card_cost_rect)
                self.card_image_mask.blit(active_card_cost_image, active_card_cost_image_rect)
        elif self.active_card_cost < self.card_cost:
            active_card_cost_image = self.active_card_cost_font.render(str(self.active_card_cost), True,
                                                                       self.main_game.settings.card_mask_font_color2)
            active_card_cost_image_rect = active_card_cost_image.get_rect(center=self.active_card_cost_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_card_cost_rect)
            self.card_image_mask.blit(active_card_cost_image, active_card_cost_image_rect)
        elif self.active_card_cost > self.card_cost:
            active_card_cost_image = self.active_card_cost_font.render(str(self.active_card_cost), True,
                                                                       self.main_game.settings.card_mask_font_color1)
            active_card_cost_image_rect = active_card_cost_image.get_rect(center=self.active_card_cost_rect.center)
            self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_card_cost_rect)
            self.card_image_mask.blit(active_card_cost_image, active_card_cost_image_rect)

        if self.card_type == "盟友":
            # 画活跃意志力
            if self.active_willpower < self.willpower:
                active_willpower_image = self.active_willpower_font.render(str(self.active_willpower), True,
                                                                           self.main_game.settings.card_mask_font_color1)
                active_willpower_image_rect = active_willpower_image.get_rect(center=self.active_willpower_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_willpower_rect)
                self.card_image_mask.blit(active_willpower_image, active_willpower_image_rect)
            elif self.active_willpower > self.willpower:
                active_willpower_image = self.active_willpower_font.render(str(self.active_willpower), True,
                                                                           self.main_game.settings.card_mask_font_color2)
                active_willpower_image_rect = active_willpower_image.get_rect(center=self.active_willpower_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background, self.active_willpower_rect)
                self.card_image_mask.blit(active_willpower_image, active_willpower_image_rect)

            # 画活跃攻击力
            if self.active_attack_force < self.attack_force:
                active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_attack_force_image_rect = active_attack_force_image.get_rect(
                    center=self.active_attack_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_attack_force_rect)
                self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)
            elif self.active_attack_force > self.attack_force:
                active_attack_force_image = self.active_attack_force_font.render(str(self.active_attack_force), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_attack_force_image_rect = active_attack_force_image.get_rect(
                    center=self.active_attack_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_attack_force_rect)
                self.card_image_mask.blit(active_attack_force_image, active_attack_force_image_rect)

            # 画活跃防御力
            if self.active_defense_force < self.defense_force:
                active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                                   self.main_game.settings.card_mask_font_color1)
                active_defense_force_image_rect = active_defense_force_image.get_rect(
                    center=self.active_defense_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_defense_force_rect)
                self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)
            elif self.active_defense_force > self.defense_force:
                active_defense_force_image = self.active_defense_force_font.render(str(self.active_defense_force), True,
                                                                                   self.main_game.settings.card_mask_font_color2)
                active_defense_force_image_rect = active_defense_force_image.get_rect(
                    center=self.active_defense_force_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_defense_force_rect)
                self.card_image_mask.blit(active_defense_force_image, active_defense_force_image_rect)

            # 画活跃生命值
            if self.active_health_point < self.health_point:
                active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                                 self.main_game.settings.card_mask_font_color1)
                active_health_point_image_rect = active_health_point_image.get_rect(
                    center=self.active_health_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_health_point_rect)
                self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)
            elif self.active_health_point > self.health_point:
                active_health_point_image = self.active_health_point_font.render(str(self.active_health_point), True,
                                                                                 self.main_game.settings.card_mask_font_color2)
                active_health_point_image_rect = active_health_point_image.get_rect(
                    center=self.active_health_point_rect.center)
                self.card_image_mask.fill(self.main_game.settings.card_mask_font_background,
                                          self.active_health_point_rect)
                self.card_image_mask.blit(active_health_point_image, active_health_point_image_rect)

        draw_condition(self)  # 画卡牌状态

    # 重置卡牌
    def reset_card(self):
        self.card_order = [None, 0, 0, None, 0, 0]
        self.order_exception = False
        self.pause_card = None
        self.pause_card_order = None
        self.copy_information = None
        if self.card_type == "盟友":
            self.active_card_cost = self.card_cost  # 重置活跃卡牌费用
            self.active_willpower = self.willpower  # 重置活跃意志力
            self.active_attack_force = self.attack_force  # 重置活跃攻击力
            self.active_defense_force = self.defense_force  # 重置活跃防御力
            self.active_health_point = self.health_point  # 重置活跃生命值
        elif self.card_type == "附属":
            self.active_card_cost = self.card_cost  # 重置活跃卡牌费用
        elif self.card_type == "事件":
            self.active_card_cost = self.card_cost  # 重置活跃卡牌费用
        self.active_condition = {}  # 重置这张卡片上的状态

    # 卡牌被选中时，导入卡牌按钮树
    def import_button(self):
        button_1 = []
        for condition in self.active_condition:
            if self.active_condition[condition]:
                button_1_X = []
                for target in self.active_condition[condition]:
                    button_1_X.append((str(target), None))
            else:
                button_1_X = None
            button_1.append((condition, button_1_X))
        button_2 = [("费用:" + str(self.active_card_cost), None)]
        if self.card_type == "盟友":
            button_2.append(("意志力:" + str(self.active_willpower), None))
            button_2.append(("攻击力:" + str(self.active_attack_force), None))
            button_2.append(("防御力:" + str(self.active_defense_force), None))
            button_2.append(("生命值:" + str(self.active_health_point), None))
        button = [("查看状态", button_1), ("查看属性", button_2)]
        if self.main_game.threat_area.current_phase == 1 and (
                self.card_type == "盟友" or self.card_type == "附属") and self in self.main_game.hand_area.card_group:
            button.insert(0, ("打出", None))
        elif self.main_game.threat_area.current_phase == 2 and self.main_game.threat_area.current_step == 0 and not self.main_game.threat_area.action_window and self.card_type == "盟友" and self in self.main_game.role_area.card_group and "已横置" not in self.active_condition and "任务中" not in self.active_condition:
            button.insert(0, ("指派", None))
        elif self.main_game.threat_area.action_window and self.card_type == "事件" and self in self.main_game.hand_area.card_group and "行动" in self.rule_mark:
            button.insert(0, ("打出", None))
        elif self.main_game.threat_area.action_window and self.card_type == "事件" and self in self.main_game.hand_area.card_group and "任务行动" in self.rule_mark and self.main_game.threat_area.current_phase == 2:
            button.insert(0, ("打出", None))
        elif self.main_game.threat_area.action_window and self.card_type == "事件" and self in self.main_game.hand_area.card_group and "战斗行动" in self.rule_mark and self.main_game.threat_area.current_phase == 5:
            button.insert(0, ("打出", None))
        elif self.main_game.threat_area.action_window and self.main_game.on_spot(
                self) and "行动" in self.rule_mark and "已横置" not in self.active_condition and "行动后" not in self.active_condition and "暗影牌" not in self.active_condition:
            button.insert(0, ("行动", None))
        elif self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 1 and not self.main_game.threat_area.action_window and self.card_type == "盟友" and self in self.main_game.role_area.card_group and "宣告防御" not in self.active_condition and "已横置" not in self.active_condition:
            button.insert(0, ("宣告防御", None))
        elif self.main_game.threat_area.current_phase == 5 and self.main_game.threat_area.current_step == 4 and not self.main_game.threat_area.action_window and self.card_type == "盟友" and self in self.main_game.role_area.card_group and "宣告攻击" not in self.active_condition and "已横置" not in self.active_condition and hasattr(
                self.main_game.threat_area, "enemy") and self.main_game.threat_area.enemy:
            button.insert(0, ("宣告攻击", None))
        self.main_game.button_option.import_button(self, button)

    # 卡牌被选中时，侦听按钮树的选项选择
    def listening_button(self):
        if self.main_game.button_option.option // 100000:
            for (num, button) in enumerate(self.main_game.button_option.buttons):
                if button[0] == "打出" and num + 1 == self.main_game.button_option.option // 100000:
                    if type(self.active_card_cost) == int:
                        self.card_order = ["打出", 0, 0, False, 0, 0]
                    elif type(self.active_card_cost) == str and self.active_card_cost[0] == "X":
                        self.card_order = ["选定X费", 0, 0, False, 0, 0]
                elif button[0] == "指派" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["指派", 0, 0, False, 0, 0]
                elif button[0] == "行动" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["行动", 0, 0, False, 0, 0]
                elif button[0] == "宣告防御" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["宣告防御", 0, 0, False, 0, 0]
                elif button[0] == "宣告攻击" and num + 1 == self.main_game.button_option.option // 100000:
                    self.card_order = ["宣告攻击", 0, 0, False, 0, 0]
            self.main_game.button_option.reset()
            self.main_game.select_card = None

    # 卡牌侦听
    def card_listening(self):
        if self.card_type == "盟友" and not self.active_health_point:
            self.active_health_point = -1
            self.card_order = ["被消灭", 0, 0, False, 0, 0]

    # 卡牌的动作循环
    def run_card_order(self):
        if self.card_order[0] == "选定X费" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[0] = None
            elif not self.main_game.information:
                point = 0
                cards = []
                for hero in self.main_game.role_area.hero_group:
                    if self.faction_symbol == "中立" or self.faction_symbol == hero.resource_symbol or "资源符+" in hero.active_condition and self.faction_symbol in \
                            hero.active_condition["资源符+"]:
                        cards.append(hero)
                for hero in cards:
                    point += hero.active_resource
                if len(self.active_card_cost) > 2 and self.active_card_cost[1] == "-":
                    point += int(self.active_card_cost[2:])
                elif len(self.active_card_cost) > 2 and self.active_card_cost[1] == "+":
                    point -= int(self.active_card_cost[2:])
                if point < 0:
                    self.card_order[0] = None
                else:
                    cards = []
                    for num in range(point + 1):
                        card = Print_Card(self.main_game)
                        card.card_target = num
                        card.card_image = self.main_game.player_card_image.copy()
                        card_rect = card.card_image.get_rect()
                        font = pygame.font.Font(
                            os.path.join(self.main_game.main_path, self.main_game.settings.font_file), card_rect.h // 3)
                        font_image = font.render(str(num), True, self.main_game.settings.card_mask_font_color3)
                        font_image_rect = font_image.get_rect(center=card_rect.center)
                        card.card_image.blit(font_image, font_image_rect)
                        cards.append(card)
                    self.select_value = self.main_game.card_select(cards).card_target
                    num = self.select_value
                    if len(self.active_card_cost) > 2 and self.active_card_cost[1] == "-":
                        num -= int(self.active_card_cost[2:])
                        if num < 0:
                            num = 0
                    elif len(self.active_card_cost) > 2 and self.active_card_cost[1] == "+":
                        num += int(self.active_card_cost[2:])
                    self.temporary_card_cost = self.active_card_cost
                    self.active_card_cost = num
                    self.update_mask()
                    self.card_order = ["打出", 0, 0, False, 0, 0]
        elif self.card_order[0] == "打出" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                point = 0
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if self.faction_symbol == "中立" or self.faction_symbol == hero.resource_symbol or "资源符+" in hero.active_condition and self.faction_symbol in \
                            hero.active_condition["资源符+"]:
                        heros.append(hero)
                for hero in heros:
                    point += hero.active_resource
                # 卡牌打出失败
                if not heros or point < self.active_card_cost or self.main_game.unique_detection(self):
                    self.card_order[0] = None
                    return
                # END
                self.deduction_heros = []
                for hero in heros:
                    self.deduction_heros.append([hero, 0])
                point = self.active_card_cost
                while point:
                    for hero in self.deduction_heros:
                        if hero[0].active_resource > hero[1] and not random.randrange(len(heros)):
                            hero[1] += 1
                            point -= 1
                            if not point:
                                break
                self.main_game.information = [0, "玩家将要打出卡牌", self]
                self.card_order[3] = True
                self.card_order[4] = 0
                self.card_order[5] = 0
                self.card_order[1] += 1
        elif self.card_order[0] == "打出" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information and self.card_order[3]:
                if self.main_game.caps_lock:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                        self.card_order[5] -= 1
                        if type(self.deduction_heros[0]) != list:
                            select_hero = self.deduction_heros.pop(0)
                            for hero in self.deduction_heros:
                                if hero[0] == select_hero:
                                    hero[1] -= 1
                                    break
                    elif self.card_order[4] % 2:
                        if type(self.deduction_heros[0]) != list:
                            select_hero = self.deduction_heros.pop(0)
                            for hero in self.deduction_heros:
                                if hero[0] == select_hero:
                                    hero[1] -= 1
                                    hero[0].active_resource -= 1
                                    if hero[0].active_resource < 0:
                                        hero[0].active_resource = 0
                                    hero[0].update_mask()
                                    self.main_game.information = [0, "英雄支付费用后", self, hero[0]]
                                    break
                        self.card_order[4] += 1
                    else:
                        point = 0
                        heros = []
                        for hero in self.deduction_heros:
                            point += hero[1]
                            heros.append(hero[0])
                        if point > 0:
                            hero = self.main_game.card_select(heros)
                            if hero.active_resource > 0:
                                self.deduction_heros.insert(0, hero)
                                self.main_game.information = [0, "英雄将要支付费用", self, hero]
                                self.card_order[4] += 1
                            else:
                                return
                        else:
                            del self.deduction_heros
                            self.main_game.information = [0, "玩家成功打出卡牌后", self]
                            if self.card_type == "附属":
                                self.card_order = ["打出附属后", 0, 0, False, 0, 0]
                            elif self.card_type == "事件":
                                self.card_order = ["打出事件后", 0, 0, False, 0, 0]
                            else:
                                self.card_order[3] = False
                                self.card_order[4] = 0
                                self.card_order[5] = 0
                                self.card_order[1] += 1
                else:
                    if self.card_order[5]:
                        self.card_order[4] += 1
                        self.card_order[5] -= 1
                        for hero in self.deduction_heros:
                            if hero[1] > 0:
                                hero[1] -= 1
                                break
                    elif self.card_order[4] % 2:
                        for hero in self.deduction_heros:
                            if hero[1] > 0:
                                hero[1] -= 1
                                hero[0].active_resource -= 1
                                if hero[0].active_resource < 0:
                                    hero[0].active_resource = 0
                                hero[0].update_mask()
                                self.main_game.information = [0, "英雄支付费用后", self, hero[0]]
                                break
                        self.card_order[4] += 1
                    else:
                        for hero in self.deduction_heros:
                            if hero[1] > 0:
                                self.main_game.information = [0, "英雄将要支付费用", self, hero[0]]
                                self.card_order[4] += 1
                                return
                        del self.deduction_heros
                        self.main_game.information = [0, "玩家成功打出卡牌后", self]
                        if self.card_type == "附属":
                            self.card_order = ["打出附属后", 0, 0, False, 0, 0]
                        elif self.card_type == "事件":
                            self.card_order = ["打出事件后", 0, 0, False, 0, 0]
                        else:
                            self.card_order[3] = False
                            self.card_order[4] = 0
                            self.card_order[5] = 0
                            self.card_order[1] += 1
        elif self.card_order[0] == "打出" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要放置进场", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "打出" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.role_area.card_group[self] = self.main_game.hand_area.card_group.pop(self)
                self.main_game.information = [0, "盟友卡牌放置进场后", self, self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "指派" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要执行任务", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "指派" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.active_condition["任务中"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌执行任务后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要宣告防御", self, self.main_game.threat_area.enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告防御" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.enemy.active_condition["攻击中"].append(self)
                self.active_condition["宣告防御"] = [self.main_game.threat_area.enemy]
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌宣告防御后", self, self.main_game.threat_area.enemy]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要横置", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.active_condition["已横置"] = None
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌横置后", self, self]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要宣告攻击", self, self.main_game.threat_area.enemy]
                self.card_order[1] += 1
        elif self.card_order[0] == "宣告攻击" and self.card_order[1] == 3:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.threat_area.enemy.active_condition["防御中"].append(self)
                self.active_condition["宣告攻击"] = [self.main_game.threat_area.enemy]
                self.update_mask()
                self.main_game.information = [0, "盟友卡牌宣告攻击后", self, self.main_game.threat_area.enemy]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌将要被消灭", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被消灭" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "盟友卡牌被消灭后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                self.main_game.information = [0, self.card_type + "卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "被弃除" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, self.card_type + "卡牌被弃除后", self]
                self.card_order = ["离场", 0, 0, False, 0, 0, "弃牌堆"]
        elif self.card_order[0] == "离场" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌将要离场", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "离场" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                our_affiliate = []
                enemy_affiliate = []
                target_affiliate = []
                if self.main_game.card_estimate(self)[self]:
                    for card in self.main_game.card_estimate(self)[self]:
                        if card.card_order[0]:
                            return
                        if card.card_type == "目标":
                            target_affiliate.append(card)
                        elif self.main_game.player_control(card):
                            our_affiliate.append(card)
                        else:
                            enemy_affiliate.append(card)
                if self.main_game.on_spot(self):
                    self.main_game.information = [0, self.card_type + "卡牌离场后", self]
                self.main_game.card_estimate(self).pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    for card in our_affiliate:
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, card)
                    if self.card_order[-1] == "弃牌堆":
                        self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = []
                    if self.card_order[-1] == "弃牌堆":
                        self.main_game.playerdiscard_area.playerdiscard_deck.append(self)
                    self.main_game.playerdiscard_area.playerdiscard_deck.extend(our_affiliate)
                if self.main_game.encounterdiscard_area.encounterdiscard_deck:
                    for card in enemy_affiliate:
                        self.main_game.encounterdiscard_area.encounterdiscard_deck.insert(0, card)
                else:
                    self.main_game.encounterdiscard_area.encounterdiscard_deck = enemy_affiliate
                for target in target_affiliate:
                    target.reset_card()
                    target.update_mask()
                    self.main_game.scenario_area.card_group[target] = None
                if self.card_order[-1] == "手牌":
                    self.reset_card()
                    self.update_mask()
                    self.main_game.hand_area.card_group[self] = None
                elif self.card_order[-1] == "牌组":
                    self.reset_card()
                    self.update_mask()
                    if self.main_game.playerdeck_area.player_deck:
                        self.main_game.playerdeck_area.player_deck.append(self)
                        random.shuffle(self.main_game.playerdeck_area.player_deck)
                    else:
                        self.main_game.playerdeck_area.player_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]


# 按钮选项的类
class Button_Option:
    def __init__(self, main_game):
        self.main_game = main_game
        self.buttons = None  # 这个变量用于放置按钮选项的树形结构(最大支持6层，每层最多支持9个选项)
        self.option = 0  # 这个变量用于存放当前选项标志，本身是一个6位数的十进制整数值
        self.current_button = None  # 用于显示的当前按钮列表
        self.importer = None  # 这个变量记录当前按钮树的导入者以防止重复导入

    # 传入按钮树
    def import_button(self, importer, buttons):
        if self.importer != importer:
            self.reset()
            self.importer = importer
            self.buttons = buttons
            self._set_current_button()

    # 用于处理键盘上的按键
    def keystroke_handling(self, event):
        key = 0
        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
            key = 1
        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
            key = 2
        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
            key = 3
        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
            key = 4
        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
            key = 5
        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
            key = 6
        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
            key = 7
        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
            key = 8
        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
            key = 9
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
            if self.option:
                self.option = self.option // 10
                self._set_current_button()
            elif self.main_game.xuanxiang:
                self.main_game.button_option.reset()
                self.main_game.select_card = None
        # 根据输入按钮设置option和current_button
        if key and self.buttons:
            if not self.option and key <= len(self.buttons):
                if self.buttons[key - 1][1]:
                    self.option = key
                    self._set_current_button()
                else:
                    self.option = key * 100000
                    self.current_button = None
            elif self.option > 0 and self.option < 10 and key <= len(self.buttons[self.option - 1][1]):
                if self.buttons[self.option - 1][1][key - 1][1]:
                    self.option = self.option * 10 + key
                    self._set_current_button()
                else:
                    self.option = self.option * 100000 + key * 10000
                    self.current_button = None
            elif self.option > 9 and self.option < 100 and key <= len(
                    self.buttons[self.option // 10 - 1][1][self.option % 10 - 1][1]):
                if self.buttons[self.option // 10 - 1][1][self.option % 10 - 1][1][key - 1][1]:
                    self.option = self.option * 10 + key
                    self._set_current_button()
                else:
                    self.option = self.option * 10000 + key * 1000
                    self.current_button = None
            elif self.option > 99 and self.option < 1000 and key <= len(
                    self.buttons[self.option // 100 - 1][1][self.option // 10 % 10 - 1][1][self.option % 10 - 1][1]):
                if self.buttons[self.option // 100 - 1][1][self.option // 10 % 10 - 1][1][self.option % 10 - 1][1][
                    key - 1][1]:
                    self.option = self.option * 10 + key
                    self._set_current_button()
                else:
                    self.option = self.option * 1000 + key * 100
                    self.current_button = None
            elif self.option > 999 and self.option < 10000 and key <= len(
                    self.buttons[self.option // 1000 - 1][1][self.option // 100 % 10 - 1][1][
                        self.option // 10 % 10 - 1][1][self.option % 10 - 1][1]):
                if \
                        self.buttons[self.option // 1000 - 1][1][self.option // 100 % 10 - 1][1][
                            self.option // 10 % 10 - 1][1][
                            self.option % 10 - 1][1][key - 1][1]:
                    self.option = self.option * 10 + key
                    self._set_current_button()
                else:
                    self.option = self.option * 100 + key * 10
                    self.current_button = None
            elif self.option > 9999 and self.option < 100000 and key <= len(
                    self.buttons[self.option // 10000 - 1][1][self.option // 1000 % 10 - 1][1][
                        self.option // 100 % 10 - 1][1][self.option // 10 % 10 - 1][1][self.option % 10 - 1][1]):
                if \
                        self.buttons[self.option // 10000 - 1][1][self.option // 1000 % 10 - 1][1][
                            self.option // 100 % 10 - 1][
                            1][self.option // 10 % 10 - 1][1][self.option % 10 - 1][1][key - 1][1]:
                    self.option = self.option * 10 + key
                    self._set_current_button()
                else:
                    self.option = self.option * 10 + key
                    self.current_button = None
        # END

    # 用于显示当前按钮选项
    def display_button(self):
        if self.current_button:
            font = pygame.font.Font(os.path.join(self.main_game.main_path, self.main_game.settings.font_file),
                                    self.main_game.settings.screen_height // 15)
            font_max_height = font.get_height()
            font_min_height = self.main_game.settings.screen_height // 100
            if font_min_height <= 0:
                font_min_height = 1
            font_height = int(
                (font_min_height - font_max_height) / 99 * len(self.current_button) + (
                        100 * font_max_height - font_min_height) / 99)
            if font_height <= 0:
                font_height = 1
            button_number = 0
            for button in self.current_button:
                font_image = font.render(button, True, self.main_game.settings.font_color,
                                         self.main_game.settings.font_color_background)
                font_rect = font_image.get_size()
                font_image = pygame.transform.scale(font_image,
                                                    (int(font_rect[0] * font_height / font_rect[1]),
                                                     font_height)).convert()
                font_image_rect = font_image.get_rect(centerx=self.main_game.screen_rect.centerx)
                button_number += 1
                font_image_rect.centery = int(
                    button_number * self.main_game.settings.screen_height / (len(self.current_button) + 1))
                self.main_game.screen.blit(font_image, font_image_rect)

    # 用于重置Button_Option的所有属性
    def reset(self):
        self.buttons = None
        self.option = 0
        self.current_button = None
        self.importer = None

    # 根据当前option设置其current_button
    def _set_current_button(self):
        self.current_button = []
        if not self.option:
            for (num, button) in enumerate(self.buttons, 1):
                self.current_button.append("(" + str(num) + ")" + button[0])
        elif self.option > 0 and self.option < 10:
            for (num, button) in enumerate(self.buttons[self.option - 1][1], 1):
                self.current_button.append("(" + str(num) + ")" + button[0])
        elif self.option > 9 and self.option < 100:
            for (num, button) in enumerate(self.buttons[self.option // 10 - 1][1][self.option % 10 - 1][1], 1):
                self.current_button.append("(" + str(num) + ")" + button[0])
        elif self.option > 99 and self.option < 1000:
            for (num, button) in enumerate(
                    self.buttons[self.option // 100 - 1][1][self.option // 10 % 10 - 1][1][self.option % 10 - 1][1], 1):
                self.current_button.append("(" + str(num) + ")" + button[0])
        elif self.option > 999 and self.option < 10000:
            for (num, button) in enumerate(self.buttons[self.option // 1000 - 1][1][self.option // 100 % 10 - 1][1][
                                               self.option // 10 % 10 - 1][1][self.option % 10 - 1][1], 1):
                self.current_button.append("(" + str(num) + ")" + button[0])
        elif self.option > 9999 and self.option < 100000:
            for (num, button) in enumerate(self.buttons[self.option // 10000 - 1][1][self.option // 1000 % 10 - 1][1][
                                               self.option // 100 % 10 - 1][1][self.option // 10 % 10 - 1][1][
                                               self.option % 10 - 1][1], 1):
                self.current_button.append("(" + str(num) + ")" + button[0])


class Program_Entrance:
    """总程序"""

    def __init__(self):
        pygame.init()
        self.main_path = os.path.split(os.path.abspath(__file__))[0]
        self.settings = settings.Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        self.screen_rect = self.screen.get_rect()
        self.xuanxiang = None  # 记录玩家在开始界面的选项
        self.player_card_image = None  # 玩家卡牌的背面图案
        self.computer_card_image = None  # 电脑卡牌的背面图案
        self.resource_image = None  # 英雄资源池的图案
        self.mouse_pos = (0, 0)  # 用于保存当前鼠标位置
        self.mouse_click = None  # 用于保存当前鼠标单击位置
        self.mouse_rightclick = None  # 用于保存当前鼠标右击位置
        self.next_step = 0  # 记录空格按键，并用这个按键来进行游戏的下一个步骤
        self.return_phase = None  # 记录回车按键，这个按键按下后将跳回当前阶段
        self.caps_lock = False  # 记录caps lock键的按下状态，决定打出卡牌时要不要手动扣费
        self.select_card = None  # 这个变量记录当前选中的卡牌
        self.response_pause = None  # 用于当卡牌响应时暂停事件行动窗口
        self.response_conflict = None  # 用于应对卡牌效果和其他卡牌的响应之间的冲突
        self.button_option = Button_Option(self)  # 初始化按钮选项的类实例
        self.information = None  # 所有卡牌交流的信息榜，第一个数值是这是第几遍播报，第二个字符串是消息，第三个是来源卡牌，第四个(有的话)是目标卡牌
        self.run_order = True  # 用于在有卡牌动作运行时暂停游戏主动作循环
        self.multiple_defender = False  # 多防御者开关，为True时表示一个敌军可以选定多名角色防御

    # 这个函数负责运行游戏的开始界面
    def start_game(self):
        button_10000 = (("简单难度", None), ("普通难度", None), ("噩梦难度", None))
        button_1111 = (("穿越幽暗密林", button_10000), ("安度因河之旅", button_10000), ("逃离多尔哥多", button_10000))
        button_111 = (("基础版+幽暗密林的阴影", button_1111), ("凯萨督姆+矮人故乡", None), ("努曼诺尔的后裔+对抗魔影", None), ("艾辛格之声+铸戒者", None),
                      ("失落的王国+安格玛觉醒", None))
        button_11 = (("原版剧情（主游戏）", button_111), ("原著剧情（传奇扩展）", None), ("独立剧情（POD）", None))
        button_1 = (("魔戒LCG", button_11), ("自定义游戏", None))
        button = (("开始", button_1), ("计分", None), ("组牌", None))
        self.button_option.import_button("start_game", button)
        while True:
            # 输入侦测区
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.button_option.keystroke_handling(event)
            # END
            # 输入判断区
            if self.button_option.option // 100000:
                if self.button_option.option // 100 == 1111 or self.button_option.option // 100000 == 3:
                    xuanxiang = self.button_option.option
                    self.button_option.reset()
                    return xuanxiang
                else:
                    self.button_option.reset()
                    self.button_option.import_button("start_game", button)
            # END
            # 屏幕显示区
            self.screen.fill(self.settings.screen_background)
            self.button_option.display_button()
            pygame.display.flip()
            # END

    # 这个函数负责运行游戏开始后的游戏界面
    def run_game(self, xuanxiang):
        self.xuanxiang = xuanxiang
        # 初始化所有区域对象
        self.threat_area = card_area.Threat_Area(self)  # 威胁、阶段、步骤...数值区
        self.task_area = card_area.Task_Area(self)  # 任务卡牌区
        self.encounter_area = card_area.Encounter_Area(self)  # 遭遇牌组区
        self.playerdeck_area = card_area.Playerdeck_Area(self)  # 玩家牌组区
        self.encounterdiscard_area = card_area.Encounterdiscard_Area(self)  # 遭遇弃牌堆区
        self.playerdiscard_area = card_area.Playerdiscard_Area(self)  # 玩家弃牌堆区
        self.scenario_area = card_area.Scenario_Area(self)  # 场景区
        self.clash_area = card_area.Clash_Area(self)  # 交锋区
        self.role_area = card_area.Role_Area(self)  # 英雄、盟友、附属、事件牌放置区
        self.hand_area = card_area.Hand_Area(self)  # 手牌区
        self.area_group = (self.threat_area, self.task_area, self.encounter_area,
                           self.playerdeck_area, self.encounterdiscard_area, self.playerdiscard_area,
                           self.scenario_area, self.clash_area, self.role_area, self.hand_area)
        # END
        # 加载卡牌
        self.player_card_image, self.computer_card_image, self.resource_image = self._load_back_image()  # 载入卡牌图案
        self.task_area.task_deck = self._load_task_deck()  # 载入所有任务牌
        self.encounter_area.encounter_deck = self._load_encounter_deck()  # 载入所有遭遇牌
        self.role_area.hero_group, self.playerdeck_area.player_deck = self._load_player_deck()  # 载入所有玩家牌
        # END
        # 检测玩家牌组是否合规
        if len(self.role_area.hero_group) > 3:
            raise Exception("卡组中超过三名英雄")
        elif len(self.role_area.hero_group) < 1:
            raise Exception("卡组中没有英雄")
        elif self.role_area.hero_repeat_detection():
            raise Exception("卡组中有重复的独有英雄")
        elif self.playerdeck_area.card_repeat_detection():
            raise Exception("卡组中放入同名卡牌超过三张")
        # END
        # 开始游戏之前的工作
        self.task_area.initialize_task_index()  # 初始化当前任务索引
        random.shuffle(self.encounter_area.encounter_deck)  # 洗混遭遇牌组
        random.shuffle(self.playerdeck_area.player_deck)  # 洗混玩家牌组
        self.threat_area.initialize_threat()  # 设定初始威胁等级
        for hero in self.role_area.hero_group:  # 放置英雄进场
            self.role_area.card_group[hero] = None
        if self.xuanxiang % 10 == 1:  # 如果选择的是简单模式，一开始给每个英雄1点资源
            for hero in self.role_area.hero_group:
                hero.active_resource += 1
                hero.update_mask()
        for num in range(6):  # 从卡组抓取六张卡牌为初始手牌
            if self.playerdeck_area.player_deck:
                self.hand_area.card_group[self.playerdeck_area.player_deck.pop(0)] = None
        self.threat_area.order[0] = True  # 开启游戏
        # END
        # 游戏界面
        time_first = 0  # 记录鼠标双击间隔
        time_second = 0  # 记录鼠标双击间隔
        pause_action_window = None  # 用于标记是否暂停了事件行动窗口
        update_button = False  # 用于在事件窗口和卡牌动作之间更新按钮选项
        while True:
            # 输入侦测区
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        time_first = time_second
                        time_second = pygame.time.get_ticks()
                        if time_second - time_first < self.settings.mouse_dblclick_interval:
                            self.button_option.reset()
                            self.select_card = None
                            self.mouse_click = None
                            self.mouse_rightclick = None
                            if self.task_area.rect.collidepoint(event.pos):
                                self.select_card = self.card_select(self.task_area.region_card)
                            elif self.encounter_area.rect.collidepoint(event.pos):
                                self.select_card = self.card_select(self.encounter_area.encounter_affiliated)
                            elif self.playerdeck_area.rect.collidepoint(event.pos):
                                self.select_card = self.card_select(self.playerdeck_area.player_affiliated)
                            elif self.encounterdiscard_area.rect.collidepoint(event.pos):
                                self.card_select(self.encounterdiscard_area.encounterdiscard_deck)
                            elif self.playerdiscard_area.rect.collidepoint(event.pos):
                                self.card_select(self.playerdiscard_area.playerdiscard_deck)
                            elif self.threat_area.rect.collidepoint(event.pos):
                                self.card_select(self.threat_area.victory_point_deck)
                            else:
                                for area in self.area_group[6:10]:
                                    if area.rect.collidepoint(event.pos):
                                        self.select_card = self.card_select(area.card_group)
                        else:
                            self.button_option.reset()
                            self.select_card = None
                            self.mouse_rightclick = None
                            self.mouse_click = event.pos
                    elif event.button == 3:
                        self.mouse_click = None
                        self.mouse_rightclick = event.pos
                elif event.type == pygame.KEYDOWN:
                    self.button_option.keystroke_handling(event)
                    if event.key == pygame.K_SPACE:
                        self.next_step = 1
                        self.button_option.reset()
                        self.select_card = None
                    elif event.key == pygame.K_RETURN and self.response_conflict is None:
                        self.return_phase = self.threat_area.current_phase
                        self.button_option.reset()
                        self.select_card = None
                    if event.mod & pygame.KMOD_CAPS:
                        self.caps_lock = True
                    else:
                        self.caps_lock = False
            # END
            # 屏幕显示区
            self.screen.fill(self.settings.screen_background)
            for area in self.area_group:
                area.display_draw()
            self.button_option.display_button()
            pygame.display.flip()
            # END
            # 动作循环区
            for area in self.area_group[1:]:  # 运行场上所有卡牌的侦听与其动作
                area.cards_listening()
                area.run_cards_order()
            if self.response_pause == True:  # 卡牌响应时暂停事件行动窗口
                if self.threat_area.action_window:
                    pause_action_window = True
                    self.threat_area.action_window = False
                self.response_conflict = True
                self.response_pause = None
            elif self.response_pause == False:  # 卡牌响应暂停的事件行动窗口的恢复
                if pause_action_window:
                    pause_action_window = False
                    self.threat_area.action_window = True
                self.response_conflict = None
                self.response_pause = None
            if self.run_order:
                if update_button:
                    update_button = False
                    self.select_card = None
                    self.button_option.reset()
                if self.select_card:
                    self.select_card.import_button()
                    self.select_card.listening_button()
                else:
                    self.threat_area.listening_action_window()  # 运行事件行动窗口
                self.threat_area.run_order()  # 运行游戏七阶段循环
            else:
                if not update_button:
                    update_button = True
                    self.select_card = None
                    self.button_option.reset()
            self.threat_area.test_game_over()  # 测试玩家是否输掉了游戏
            # END
            # 消息公示递减
            if self.information:  # 播报两遍确定消息被所有函数侦听，然后删除消息
                if self.information[0] < 2:
                    self.information[0] += 1
                else:
                    self.information = None
            if self.return_phase is None and self.next_step:  # 下一步指示
                if self.next_step > 2:
                    self.next_step = 0
                else:
                    self.next_step += 1
            elif self.return_phase and self.threat_area.current_phase == self.return_phase:  # 跳过阶段
                self.next_step = 1
            elif self.return_phase and self.threat_area.current_phase != self.return_phase:  # 结束跳过阶段
                self.next_step = 0
                self.return_phase = None
            self.run_order = True  # 尝试运行游戏主动作循环，看看接下来会不会被卡牌动作打断
            # END
        # END

    # 卡牌选择器
    def card_select(self, cards):
        if type(cards) == dict:  # 将字典里的卡牌及其附属都放进一个列表中
            cards_list = []
            for card in cards.keys():
                cards_list.append(card)
                if cards[card]:
                    cards_list.extend(cards[card])
            cards = cards_list
        card_height = (
                              self.settings.screen_height - self.settings.screen_height * 2 * self.settings.card_select_hnumber / self.settings.area_height_spacing) / self.settings.card_select_hnumber
        card_width = int(card_height * self.settings.original_card_size[0] / self.settings.original_card_size[1])
        card_height = int(card_height)
        card_select_wnumber = int(self.settings.area_width_spacing * self.settings.screen_width / (
                self.settings.area_width_spacing * card_width + 2 * self.settings.screen_width))
        num = 0
        card = None
        cards_list = []
        while cards and card_select_wnumber and num < len(cards):
            card = []
            for number in range(card_select_wnumber):
                if num < len(cards):
                    card.append(cards[num])
                    num += 1
            cards_list.append(card)
        index = 0
        while cards:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.select_card = None
                        self.mouse_rightclick = None
                        self.mouse_click = event.pos
                    elif event.button == 3:
                        self.mouse_click = None
                        self.mouse_rightclick = event.pos
                    elif event.button == 4:
                        if index > 0:
                            index -= 1
                    elif event.button == 5:
                        if index < len(cards_list) - self.settings.card_select_hnumber:
                            index += 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if index > 0:
                            index -= 1
                    elif event.key == pygame.K_DOWN:
                        if index < len(cards_list) - self.settings.card_select_hnumber:
                            index += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_PAGEUP:
                        while index > 0:
                            index -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_PAGEDOWN:
                        while index < len(cards_list) - self.settings.card_select_hnumber:
                            index += 1
            self.screen.fill(self.settings.screen_background)
            for num in range(self.settings.card_select_hnumber):
                if index + num < len(cards_list):
                    for number in range(card_select_wnumber):
                        if number < len(cards_list[index + num]):
                            card_image = pygame.transform.scale(cards_list[index + num][number].card_image,
                                                                (card_width, card_height))
                            card_image_rect = card_image.get_rect(center=(
                                self.settings.screen_width * (number * 2 + 1) / 2 / card_select_wnumber,
                                self.settings.screen_height * (num * 2 + 1) / 2 / self.settings.card_select_hnumber))
                            # 如果鼠标单击了这张卡牌，返回这张卡牌
                            if self.mouse_click and card_image_rect.collidepoint(self.mouse_click):
                                self.mouse_click = None
                                return cards_list[index + num][number]
                            # 如果鼠标右击了这张卡牌，将此卡牌载入卡牌展示器展示
                            if self.mouse_rightclick and card_image_rect.collidepoint(self.mouse_rightclick):
                                self.card_exhibition(cards_list[index + num][number])
                                self.mouse_rightclick = None
                            # 鼠标悬停可选区域上时让卡牌提高显示
                            if card_image_rect.collidepoint(self.mouse_pos):
                                card_image_rect.y -= card_image_rect.h // self.settings.card_enhance_scale
                            self.screen.blit(card_image, card_image_rect)
                            card_image_mask = pygame.transform.scale(
                                cards_list[index + num][number].card_image_mask, (card_width, card_height))
                            self.screen.blit(card_image_mask, card_image_rect)
            pygame.display.flip()
        return card

    # 卡牌展示器
    def card_exhibition(self, card, time=0):
        """
        英雄的初始威胁值/卡牌费用/卡牌交锋值/任务序号      卡牌名称/是否为独有牌/任务名称
        意志力/威胁力                                 遭遇符号/影响力派系符号/遭遇信息
        攻击力                                       卡牌属性文字/剧情名称
        防御力                                       卡牌胜利点
        生命值/任务点                                 卡牌类型
        """
        self.screen.fill(self.settings.screen_background)
        if card.card_type == "任务":
            card_image = pygame.transform.smoothscale(card.card_image, (
                self.settings.screen_height * self.settings.original_card_size[1] // self.settings.original_card_size[
                    0] // 2,
                self.settings.screen_height // 2))
        else:
            card_image = pygame.transform.smoothscale(card.card_image, (
                self.settings.screen_height * self.settings.original_card_size[0] // self.settings.original_card_size[
                    1] // 2,
                self.settings.screen_height // 2))
        card_rect = card_image.get_rect(midtop=self.screen_rect.midtop)
        self.screen.blit(card_image, card_rect)

        text_rect_1 = pygame.Rect(0, 0, (self.settings.screen_width - card_rect.w) // 2, card_rect.h)
        text_rect_2 = pygame.Rect(card_rect.right, 0, (self.settings.screen_width - card_rect.w) // 2, card_rect.h)
        text_rect_3 = pygame.Rect(0, card_rect.bottom, self.settings.screen_width,
                                  self.settings.screen_height - card_rect.h)
        text = list(range(10))
        unique_symbol = ""
        if card.card_type == "英雄":
            if card.unique_symbol:
                unique_symbol = "(独有)"
            text[0] = "威胁:" + str(card.initial_threat)
            text[1] = "意志:" + str(card.willpower)
            text[2] = "攻击:" + str(card.attack_force)
            text[3] = "防御:" + str(card.defense_force)
            text[4] = "生命:" + str(card.health_point)
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "派系:" + card.resource_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "盟友":
            if card.unique_symbol:
                unique_symbol = "(独有)"
            text[0] = "费用:" + str(card.card_cost)
            text[1] = "意志:" + str(card.willpower)
            text[2] = "攻击:" + str(card.attack_force)
            text[3] = "防御:" + str(card.defense_force)
            text[4] = "生命:" + str(card.health_point)
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "派系:" + card.faction_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "附属":
            if card.unique_symbol:
                unique_symbol = "(独有)"
            text[0] = "费用:" + str(card.card_cost)
            text[1] = ""
            text[2] = ""
            text[3] = ""
            text[4] = ""
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "派系:" + card.faction_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "事件":
            if card.unique_symbol:
                unique_symbol = "(独有)"
            text[0] = "费用:" + str(card.card_cost)
            text[1] = ""
            text[2] = ""
            text[3] = ""
            text[4] = ""
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "派系:" + card.faction_symbol
            text[7] = ""
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "敌军":
            text[0] = "交锋:" + str(card.clash_value)
            text[1] = "威胁:" + str(card.threat_force)
            text[2] = "攻击:" + str(card.attack_force)
            text[3] = "防御:" + str(card.defense_force)
            text[4] = "生命:" + str(card.health_point)
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "遭遇:" + card.encounter_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = "胜利点:" + str(card.victory_points)
            text[9] = "类型:" + card.card_type
        elif card.card_type == "地区":
            text[0] = ""
            text[1] = "威胁:" + str(card.threat_force)
            text[2] = ""
            text[3] = ""
            text[4] = "探索:" + str(card.task_point)
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "遭遇:" + card.encounter_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = "胜利点:" + str(card.victory_points)
            text[9] = "类型:" + card.card_type
        elif card.card_type == "阴谋":
            text[0] = ""
            text[1] = ""
            text[2] = ""
            text[3] = ""
            text[4] = ""
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "遭遇:" + card.encounter_symbol
            text[7] = ""
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "目标":
            text[0] = ""
            text[1] = ""
            text[2] = ""
            text[3] = ""
            text[4] = ""
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "遭遇:" + card.encounter_symbol
            text[7] = "属性:"
            for attribute in card.card_attribute:
                text[7] += attribute + ' '
            text[8] = ""
            text[9] = "类型:" + card.card_type
        elif card.card_type == "任务":
            text[0] = "序号:" + str(card.card_number)
            text[1] = ""
            text[2] = ""
            text[3] = ""
            if card.task_point == None:
                text[4] = ""
            else:
                text[4] = "探索:" + str(card.task_point)
            text[5] = "名称:" + unique_symbol + card.card_name
            text[6] = "遭遇:"
            for encounter in card.encounter_symbol:
                text[6] += encounter + " "
            text[7] = "剧情:" + card.plot_name
            text[8] = ""
            text[9] = "类型:" + card.card_type
        else:
            for num in range(10):
                text[num] = ""
        # 画图像左边的信息
        font_size = text_rect_1.h // 6
        while font_size > 1:
            display_font = pygame.font.Font(os.path.join(self.main_path, self.settings.font_file), font_size)
            num = 0
            for num in range(5):
                if display_font.size(text[num])[0] > text_rect_1.w:
                    num = 0
                    break
            if num:
                break
            else:
                font_size -= 1
        num = 1
        for t in text[:5]:
            t_image = display_font.render(t, True, self.settings.font_color)
            t_image_rect = t_image.get_rect()
            t_image_rect.center = (text_rect_1.centerx, num * text_rect_1.h // 6 + text_rect_1.y)
            self.screen.blit(t_image, t_image_rect)
            num += 1
        # 画图像右边的信息
        font_size = text_rect_2.h // 6
        while font_size > 1:
            display_font = pygame.font.Font(os.path.join(self.main_path, self.settings.font_file), font_size)
            num = 5
            for num in range(5, 10):
                if display_font.size(text[num])[0] > text_rect_2.w:
                    num = 0
                    break
            if num:
                break
            else:
                font_size -= 1
        num = 1
        for t in text[5:]:
            t_image = display_font.render(t, True, self.settings.font_color)
            t_image_rect = t_image.get_rect()
            t_image_rect.center = (text_rect_2.centerx, num * text_rect_2.h // 6 + text_rect_1.y)
            self.screen.blit(t_image, t_image_rect)
            num += 1

        # 画图像下边的信息
        text.clear()
        biaoji = 0
        if hasattr(card, "rule_text") and card.rule_text:
            text = card.rule_text.split('\n')
        if hasattr(card, "shadow_text") and card.shadow_text:
            text.extend(card.shadow_text.split('\n'))
        if hasattr(card, "describe_text") and card.describe_text:
            text.append(card.describe_text)
            biaoji = 1
        if text:
            font_size = text_rect_3.h // (len(text) + 1)
            while font_size > 1:
                display_font = pygame.font.Font(os.path.join(self.main_path, self.settings.font_file), font_size)
                num = 0
                t = False
                while num < len(text) - biaoji:
                    if display_font.size(text[num])[0] > text_rect_3.w:
                        t = True
                        break
                    num += 1
                if t:
                    if font_size - 1 > text_rect_3.h // (len(text) + 2 + biaoji):
                        font_size -= 1
                    else:
                        t1 = text[num][:len(text[num]) // 2]
                        t2 = text[num][len(text[num]) // 2:]
                        text[num] = t1
                        text.insert(num + 1, t2)
                else:
                    break
            num = 0
            while num < len(text) - biaoji:
                t_image = display_font.render(text[num], True, self.settings.font_color)
                t_image_rect = t_image.get_rect(centerx=text_rect_3.centerx)
                num += 1
                t_image_rect.centery = num * text_rect_3.h // (len(text) + 1 + biaoji) + text_rect_3.y
                self.screen.blit(t_image, t_image_rect)
            if biaoji:
                while font_size > 1:
                    display_font = pygame.font.Font(os.path.join(self.main_path, self.settings.font_file), font_size)
                    if display_font.size(text[num])[0] > text_rect_3.w:
                        font_size -= 1
                    else:
                        break
                display_font.set_italic(True)
                t_image = display_font.render(text[num], True, self.settings.font_color)
                t_image_rect = t_image.get_rect(centerx=text_rect_3.centerx)
                num += 1
                t_image_rect.centery = num * text_rect_3.h // (len(text) + 1 + biaoji) + text_rect_3.y
                self.screen.blit(t_image, t_image_rect)

        pygame.display.flip()
        if time:
            pygame.time.wait(time)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    if time:
                        return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

    # 检测卡牌是否是玩家控制卡牌，是则返回True，否则返回False
    def player_control(self, card):
        if card.card_type == "英雄" or card.card_type == "盟友" or card.card_type == "附属" or card.card_type == "事件":
            return True
        elif card.card_type == "目标" and "附属到" in card.active_condition:
            for kapai in card.active_condition["附属到"]:
                if self.player_control(kapai):
                    return True
            else:
                return False
        else:
            return False

    # 检测卡牌是否在场，是则返回True，否则返回False
    def on_spot(self, kapai):
        if kapai in self.role_area.card_group:
            return True
        if kapai in self.clash_area.card_group:
            return True
        if kapai in self.scenario_area.card_group:
            return True
        if kapai in self.task_area.region_card:
            return True
        if self.playerdeck_area.player_affiliated and kapai in self.playerdeck_area.player_affiliated:
            return True
        for card in self.task_area.region_card:
            if self.task_area.region_card[card] and kapai in self.task_area.region_card[card]:
                return True
        for card in self.role_area.card_group:
            if self.role_area.card_group[card] and kapai in self.role_area.card_group[card]:
                return True
        for card in self.clash_area.card_group:
            if self.clash_area.card_group[card] and kapai in self.clash_area.card_group[card]:
                return True
        for card in self.scenario_area.card_group:
            if self.scenario_area.card_group[card] and kapai in self.scenario_area.card_group[card]:
                return True
        return False

    # 卡牌的场上独有检测，返回True表示场上有同名的独有牌
    def unique_detection(self, kapai):
        if hasattr(kapai, "unique_symbol") and kapai.unique_symbol:
            for card in self.role_area.card_group:
                if kapai.card_name == card.card_name:
                    return True
                elif self.role_area.card_group[card]:
                    for card_affiliated in self.role_area.card_group[card]:
                        if kapai.card_name == card_affiliated.card_name:
                            return True
            for card in self.clash_area.card_group:
                if kapai.card_name == card.card_name:
                    return True
                elif self.clash_area.card_group[card]:
                    for card_affiliated in self.clash_area.card_group[card]:
                        if kapai.card_name == card_affiliated.card_name:
                            return True
            for card in self.scenario_area.card_group:
                if kapai.card_name == card.card_name:
                    return True
                elif self.scenario_area.card_group[card]:
                    for card_affiliated in self.scenario_area.card_group[card]:
                        if kapai.card_name == card_affiliated.card_name:
                            return True
            for card in self.task_area.region_card:
                if self.task_area.region_card[card]:
                    for card_affiliated in self.task_area.region_card[card]:
                        if kapai.card_name == card_affiliated.card_name:
                            return True
            if self.playerdeck_area.player_affiliated:
                for card in self.playerdeck_area.player_affiliated:
                    if kapai.card_name == card.card_name:
                        return True
        return False

    # 返回给定参数卡牌的所属区域的卡表字典card_group的函数
    def card_estimate(self, card):
        if card in self.hand_area.card_group:
            return self.hand_area.card_group
        elif card in self.role_area.card_group:
            return self.role_area.card_group
        elif card in self.clash_area.card_group:
            return self.clash_area.card_group
        elif card in self.scenario_area.card_group:
            return self.scenario_area.card_group
        elif card in self.task_area.region_card:
            return self.task_area.region_card
        return None

    # 游戏胜利通关的函数
    def game_victory(self):
        self.screen.fill(self.settings.screen_background)
        font = pygame.font.Font(None, self.settings.screen_height // 4)
        font_image = font.render("Victory!", True, self.settings.font_color)
        font_rect = font_image.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(font_image, font_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):
                    sys.exit()

    # 这个函数负责在游戏一开始载入所有的任务牌，并返回排序好的这些任务牌对象的列表。
    def _load_task_deck(self):
        task_path = self.main_path[:]
        task_order_file = self.main_path[:]
        task_module_path = ""
        if self.xuanxiang // 10000 % 10 == 1:
            task_path = os.path.join(task_path, "魔戒LCG")
            task_order_file = os.path.join(task_order_file, "魔戒LCG")
            task_module_path += "魔戒LCG."
        elif self.xuanxiang // 10000 % 10 == 2:
            pass  # 自定义游戏
        if self.xuanxiang // 1000 % 10 == 1:
            task_path = os.path.join(task_path, "原版剧情")
            task_module_path += "原版剧情."
        elif self.xuanxiang // 1000 % 10 == 2:
            pass  # 原著剧情...
        if self.xuanxiang // 100 % 10 == 1:
            task_path = os.path.join(task_path, "Level1")
            task_module_path += "Level1."
        elif self.xuanxiang // 100 % 10 == 2:
            pass  # Level2...
        task_path = os.path.join(task_path, "任务牌")
        task_module_path += "任务牌."
        all_file_name = os.listdir(task_path)
        input_file_name = []
        for file_name in all_file_name:
            if file_name.endswith(".py"):
                input_file_name.append(file_name[:-3])
        task_module = list(range(len(input_file_name)))
        task_deck = list(range(len(input_file_name)))
        for num in range(len(input_file_name)):
            task_module[num] = import_module(task_module_path + input_file_name[num])
            task_deck[num] = task_module[num].Task(self)
        with open(os.path.join(task_order_file, "任务顺序")) as file:
            task_order_name = file.readlines()
        task_order_deck = []
        for order_plot_name in task_order_name:
            task_order = []
            for plot in task_deck:
                if plot.plot_name == order_plot_name.rstrip('\n'):
                    task_order.append(plot)
            for num in range(len(task_order)):
                task_order_deck.append(num)
            for task in task_order:
                task_order_deck[task.card_number - len(task_order) - 1] = task

        return task_order_deck

    # 这个函数负责在游戏一开始根据任务牌上的遭遇信息载入所有遭遇牌，并返回遭遇牌对象的列表。
    def _load_encounter_deck(self):
        encounter_information = []
        encounter_deck = []
        for task in self.task_area.task_deck:
            if task.card_number == 1:
                encounter_information.append(task.encounter_symbol)
        encounter_path = self.main_path[:]
        encounter_module_path = ""
        if self.xuanxiang // 10000 % 10 == 1:
            encounter_path = os.path.join(encounter_path, "魔戒LCG")
            encounter_module_path += "魔戒LCG."
        elif self.xuanxiang // 10000 % 10 == 2:
            pass  # 自定义游戏
        if self.xuanxiang // 1000 % 10 == 1:
            encounter_path = os.path.join(encounter_path, "原版剧情")
            encounter_module_path += "原版剧情."
        elif self.xuanxiang // 1000 % 10 == 2:
            pass  # 原著剧情...
        if self.xuanxiang // 100 % 10 == 1:
            encounter_path = os.path.join(encounter_path, "Level1")
            encounter_module_path += "Level1."
        elif self.xuanxiang // 100 % 10 == 2:
            pass  # Level2...
        for encounter in encounter_information[self.xuanxiang // 10 % 10 - 1]:
            encounter_path_file = encounter_path[:]
            encounter_module_path_file = encounter_module_path[:]
            encounter_path_file = os.path.join(encounter_path_file, "电脑-" + encounter)
            encounter_module_path_file += "电脑-" + encounter + "."
            all_folder_name = [folder for folder in os.listdir(encounter_path_file) if
                               os.path.isdir(os.path.join(encounter_path_file, folder))]
            for folder in all_folder_name:
                all_file_name = os.listdir(os.path.join(encounter_path_file, folder))
                module_file_name = encounter_module_path_file + folder + "."
                for file_name in all_file_name:
                    if file_name.endswith(".py"):
                        encounter_module = import_module(module_file_name + file_name[:-3])
                        encounter_deck.append(encounter_module.Enemy(self))
                        card_amount = encounter_deck[-1].card_amount[xuanxiang % 10 - 1]
                        if card_amount > 0:
                            card_amount -= 1
                        else:
                            encounter_deck.pop()
                        while card_amount > 0:
                            encounter_deck.append(encounter_module.Enemy(self))
                            card_amount -= 1

        return encounter_deck

    # 这个函数负责在游戏一开始载入玩家所有的英雄、盟友、附属、事件牌
    def _load_player_deck(self):
        hero_group = []
        player_deck = []
        with open(os.path.join(self.main_path, "玩家牌组")) as file:
            player_card_paths = file.readlines()
        for module_path in player_card_paths:
            if len(module_path) > 4:
                module_name = import_module(module_path.strip('\n'))
                try:
                    if callable(module_name.Hero):
                        hero_group.append(module_name.Hero(self))
                except AttributeError:
                    try:
                        if callable(module_name.Player):
                            player_deck.append(module_name.Player(self))
                    except AttributeError:
                        raise

        return hero_group, player_deck

    # 这个函数负责在游戏一开始载入卡牌图案，返回图像的Surface对象
    def _load_back_image(self):
        image_path = self.main_path[:]
        if self.xuanxiang // 10000 % 10 == 1:
            image_path = os.path.join(image_path, "魔戒LCG")
        elif self.xuanxiang // 10000 % 10 == 2:
            pass
        player_image = pygame.image.load(os.path.join(image_path, "player.jpg")).convert()
        computer_image = pygame.image.load(os.path.join(image_path, "sauron.jpg")).convert()
        resource_image = pygame.image.load(os.path.join(image_path, "resource.png"))
        return player_image, computer_image, resource_image


if __name__ == "__main__":
    main_game = Program_Entrance()
    xuanxiang = main_game.start_game()
    if xuanxiang // 100000 == 1:  # 开始游戏
        main_game.run_game(xuanxiang)
    elif xuanxiang // 100000 == 2:  # 历史计分
        pass
    elif xuanxiang // 100000 == 3:  # 组牌器
        set_cards.Set_Card(main_game).run_set_card()
