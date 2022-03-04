class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        self.original_card_size = (429, 600)  # 原始卡牌的图像大小，用于建立卡牌尺寸比例的标准
        self.screen_width = 2500  # 屏幕宽度设置
        self.screen_height = 1700  # 屏幕高度设置
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen_background = (255, 255, 255)  # 屏幕背景
        self.font_file = "simsun.ttf"  # 游戏中默认使用的中文字体（当前目录下）
        self.font_color = (0, 0, 0)  # 默认使用的按钮字体颜色
        self.font_color_background = (200, 200, 200)  # 默认使用的按钮字体背景颜色
        self.area_height_spacing = 50  # 上下两个区域之间的默认间距(屏幕高的多少分之一)
        self.area_width_spacing = 100  # 左右两个区域之间的默认间距(屏幕宽的多少分之一)
        self.card_mask_font_color1 = (255, 0, 0)  # 卡牌活跃数值低于原始值时的默认字体颜色
        self.card_mask_font_color2 = (60, 179, 113)  # 卡牌活跃数值高于原始值时的默认字体颜色
        self.card_mask_font_color3 = (255, 255, 255)  # 卡牌状态及资源的默认字体颜色
        self.card_mask_font_background = (255, 255, 255)  # 卡牌活跃数值的默认字体背景颜色
        self.threat_area_background = (255, 255, 255)  # 威胁面板区域的默认背景颜色
        self.card_condition_hnumber = 6  # 卡牌状态框总计显示多少个当前状态
        self.card_select_hnumber = 3  # 卡牌选择器一列显示多少张卡牌
        self.card_enhance_scale = 8  # 附属卡牌上或者鼠标悬停在卡牌上时，卡牌提高其高度的多少分之一
        self.card_exhibition_time = 1000  # 卡牌展示器默认的卡牌展示时间(毫秒)
        self.mouse_dblclick_interval = 300  # 鼠标双击的判定间隔时间(毫秒)
        self.health_point_ceiling = 99999  # 生命值上限，这个数值相当于无限大
