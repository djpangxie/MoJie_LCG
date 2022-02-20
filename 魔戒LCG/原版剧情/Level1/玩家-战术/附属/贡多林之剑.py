from main import *


class Player(Player_Group):
    def __init__(self, main_game):
        self.main_game = main_game
        self.card_dir = os.path.split(os.path.abspath(__file__))[0]  # 文件所在目录的绝对路径
        self.card_file = "贡多林之剑.jpg"  # 卡牌的图像文件名
        self.card_image = pygame.image.load(os.path.join(self.card_dir, self.card_file)).convert()  # 卡牌的原始图像
        self.card_name = "贡多林之剑"  # 卡牌的名称
        self.unique_symbol = False  # True表示卡牌为独有牌，只要此独有牌在场(弃牌堆不算)，所有玩家都不能够打出或放置第二张此卡牌
        self.card_cost = 1  # 卡牌的费用，玩家必须从对应的资源池中支付所示数量的资源才能打出该卡牌
        self.faction_symbol = "战术"  # 影响力派系符号，表示本卡牌隶属于哪个派系
        self.card_attribute = ("物品", "武器")  # 卡牌的属性文字标志，作为其他卡牌效果的目标判断
        self.rule_keyword = ("限制",)  # 卡牌的规则关键词，表示卡牌有些什么关键词
        self.rule_mark = ("响应",)  # 卡牌的规则效果标志，表示卡牌有些什么效果
        self.card_type = "附属"  # 卡牌类型，表明本卡牌是英雄、盟友、附属还是事件

        # 规则文字，本卡牌在场时的特殊能力
        self.rule_text = "限制.\n附属到一名英雄上。\n当攻击半兽人时，所附属英雄获得+1攻击力。\n响应：在所附属英雄攻击并消灭敌军后，放置1枚进度标记到当前任务上。"

        # 剧情描述的斜体文字
        self.describe_text = "能够佩带来自贡多林的武器，让他感觉到自己身在歌谣中的半兽人战争中，是个地位重要的人。 ——《哈比人》"

        super().__init__()  # 初始化基类中的各种属性位置信息

        self._increase = False
        self.attack_object = None

    # 卡牌侦听
    def card_listening(self):
        super().card_listening()
        if "附属到" in self.active_condition and "宣告攻击" in self.active_condition["附属到"][
            0].active_condition and not self._increase:
            for enemy in self.active_condition["附属到"][0].active_condition["宣告攻击"]:
                if "半兽人" in enemy.card_attribute or "属性+" in enemy.active_condition and "半兽人" in enemy.active_condition[
                    "属性+"]:
                    self.active_condition["附属到"][0].active_attack_force += 1
                    self.active_condition["附属到"][0].update_mask()
                    self._increase = True
                    break
        elif self._increase and "附属到" in self.active_condition and "宣告攻击" not in self.active_condition["附属到"][
            0].active_condition:
            self.active_condition["附属到"][0].active_attack_force -= 1
            if self.active_condition["附属到"][0].active_attack_force < 0:
                self.active_condition["附属到"][0].active_attack_force = 0
            self.active_condition["附属到"][0].update_mask()
            self._increase = False
        if "附属到" in self.active_condition and self.main_game.information and self.active_condition["附属到"][
            0].card_type + "卡牌攻击后" in self.main_game.information[1] and self.main_game.information[2] == \
                self.active_condition["附属到"][0] and self.main_game.information[3] != self.attack_object:
            self.attack_object = self.main_game.information[3]
        elif self.attack_object is not None and (
                "附属到" not in self.active_condition or "宣告攻击" not in self.active_condition["附属到"][
            0].active_condition and self.attack_object.active_health_point > 0):
            self.attack_object = None
        elif "附属到" in self.active_condition and self.active_condition["附属到"][
            0].active_health_point > 0 and "响应后" not in self.active_condition and self.main_game.information and \
                self.main_game.information[1] == "敌军卡牌被消灭后" and self.main_game.information[2] == self.attack_object:
            self.main_game.response_conflict = True
            self.card_order = ["响应", 0, 0, False, 0, 0]
            self.active_condition["响应后"] = None
            self.attack_object = None

    # 执行这张卡片的运行效果
    def run_card_order(self):
        super().run_card_order()
        if self.card_order[0] == "打出附属后" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                heros = []
                for hero in self.main_game.role_area.hero_group:
                    if "免疫" not in hero.rule_mark:
                        heros.append(hero)
                if heros:
                    self.select_hero = self.main_game.card_select(heros)
                    self.main_game.information = [0, "附属卡牌将要附属", self, self.select_hero]
                else:
                    self.card_order[2] = 1
                self.card_order[1] += 1
        elif self.card_order[0] == "打出附属后" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.main_game.hand_area.card_group.pop(self)
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self.main_game.card_estimate(self.select_hero)[self.select_hero]:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero].append(self)
                else:
                    self.main_game.card_estimate(self.select_hero)[self.select_hero] = [self]
                if "被附属" not in self.select_hero.active_condition or not self.select_hero.active_condition["被附属"]:
                    self.select_hero.active_condition["被附属"] = [self]
                else:
                    self.select_hero.active_condition["被附属"].append(self)
                self.active_condition["附属到"] = [self.select_hero]
                self.update_mask()
                self.select_hero.update_mask()
                self.main_game.information = [0, "附属卡牌附属后", self, self.select_hero]
                self.main_game.hand_area.card_group.pop(self)
                self.card_order[1] += 1
        elif self.card_order[0] == "打出附属后" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                num = 0
                affiliate = []
                for target in self.select_hero.active_condition["被附属"]:
                    if "限制" in target.rule_keyword:
                        affiliate.append(target)
                        num += 1
                if num > 2:
                    del self.select_hero
                    self.card_order = [None, 0, 0, None, 0, 0]
                    select_affiliate = self.main_game.card_select(affiliate)
                    select_affiliate.card_order = ["弃除附属", 0, 0, False, 0, 0]
                else:
                    del self.select_hero
                    self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                self.main_game.information = [0, "附属卡牌将要被弃除", self]
                self.card_order[1] += 1
        elif self.card_order[0] == "弃除附属" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order = [None, 0, 0, None, 0, 0]
            elif not self.main_game.information:
                if self._increase:
                    self.active_condition["附属到"][0].active_attack_force -= 1
                    if self.active_condition["附属到"][0].active_attack_force < 0:
                        self.active_condition["附属到"][0].active_attack_force = 0
                    self.active_condition["附属到"][0].update_mask()
                    self._increase = False
                for hero in self.active_condition["附属到"]:
                    hero.active_condition["被附属"].remove(self)
                    if not hero.active_condition["被附属"]:
                        hero.active_condition.pop("被附属")
                    self.main_game.card_estimate(hero)[hero].remove(self)
                    hero.update_mask()
                self.active_condition.pop("附属到")
                if self.main_game.playerdiscard_area.playerdiscard_deck:
                    self.main_game.playerdiscard_area.playerdiscard_deck.insert(0, self)
                else:
                    self.main_game.playerdiscard_area.playerdiscard_deck = [self]
                self.update_mask()
                self.main_game.information = [0, "附属卡牌被弃除后", self]
                self.card_order = [None, 0, 0, None, 0, 0]
        elif self.card_order[0] == "响应" and self.card_order[1] == 0:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif self.main_game.response_pause != True:
                self.main_game.response_pause = True
                self.main_game.button_option.import_button(str(self), (
                    ("响应-" + self.card_name, None), ("不响应-" + self.card_name, None)))
                if self.main_game.button_option.option // 100000 == 1:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 1
                elif self.main_game.button_option.option // 100000 == 2:
                    self.main_game.button_option.reset()
                    self.card_order[1] += 2
        elif self.card_order[0] == "响应" and self.card_order[1] == 1:
            if self.card_order[2]:
                self.card_order[1] += 1
                self.card_order[2] -= 1
            elif not self.main_game.information:
                regions = []
                for region in self.main_game.task_area.region_card:
                    if region.card_type == "地区" and "免疫" not in region.rule_mark:
                        regions.append(region)
                if regions:
                    if len(regions) > 1:
                        region = self.main_game.card_select(regions)
                    else:
                        region = regions[0]
                    region.active_task_point -= 1
                    if region.active_task_point < 0:
                        region.active_task_point = 0
                    region.update_mask()
                elif not self.main_game.task_area.region_card and "免疫" not in self.main_game.task_area.task_deck[
                    self.main_game.task_area.task_number].rule_mark:
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point -= 1
                    if self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point < 0:
                        self.main_game.task_area.task_deck[self.main_game.task_area.task_number].active_task_point = 0
                    self.main_game.task_area.task_deck[self.main_game.task_area.task_number].update_mask()
                self.card_order[1] += 1
        elif self.card_order[0] == "响应" and self.card_order[1] == 2:
            if self.card_order[2]:
                self.card_order[2] = 0
            elif not self.main_game.information:
                self.main_game.response_pause = False
                self.active_condition.pop("响应后")
                self.update_mask()
                self.card_order = [None, 0, 0, None, 0, 0]
