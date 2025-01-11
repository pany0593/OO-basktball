from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel
from match_singleton import MatchSingleton
from PyQt6.QtCore import QObject, pyqtSignal


# 定义事件管理器类
class CourtEventManager(QObject):
    # 定义自定义信号
    possession = pyqtSignal()  # 拥有球权
    foul = pyqtSignal()  # 犯规
    two_points = pyqtSignal()  # 2分进球
    three_points = pyqtSignal()  # 3分进球
    free_throw = pyqtSignal()  # 罚球
    block = pyqtSignal()  # 盖帽
    out_of_bounds = pyqtSignal()  # 球出界
    update = pyqtSignal()  # 更新

    def __init__(self, parent=None):
        super().__init__(parent)


# 创建篮球场控件
def create_court(parent, event_manager):
    court = QLabel(parent)
    court.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # 设置默认背景颜色和图片
    court.setStyleSheet(
        f"""
        background-color: lightgray;
        background-position: center;
        background-repeat: no-repeat;
        """
    )

    # 绑定事件信号到响应函数
    event_manager.possession.connect(lambda: change_background(court, "white", persistent=True))
    event_manager.foul.connect(lambda: change_background(court, "red", 1000))
    event_manager.two_points.connect(lambda: change_background(court, "lightgreen", 1000))
    event_manager.three_points.connect(lambda: change_background(court, "darkgreen", 1000))
    event_manager.free_throw.connect(lambda: change_background(court, "lightblue", 1000))
    event_manager.block.connect(lambda: change_background(court, "blue", 1000))
    event_manager.out_of_bounds.connect(lambda: change_background(court, "yellow", 1000))
    event_manager.update.connect(lambda: reset_background(court))

    return court


# 修改背景颜色的函数
def change_background(court, color, duration=0, persistent=False):
    """
    改变 court 的背景颜色。
    :param court: QLabel 实例。
    :param color: 背景颜色。
    :param duration: 颜色持续时间（毫秒）。
    :param persistent: 是否保持该颜色。
    """
    # 设置背景颜色和图片
    court.setStyleSheet(
        f"""
        background-color: {color};
        background-position: center;
        background-repeat: no-repeat;
        """
    )

    # 如果需要恢复背景颜色，设置计时器
    if not persistent and duration > 0:
        QTimer.singleShot(duration, lambda: reset_background(court))


# 恢复默认背景颜色和图片
def reset_background(court):
    """
    恢复默认的背景颜色和图片。
    :param court: QLabel 实例。
    """
    match = MatchSingleton.get_instance()
    background_image = match.get_icon(court)

    court.setStyleSheet(
        f"""
        background-color: lightgray;
        background-image: url({background_image});
        background-position: center;
        background-repeat: no-repeat;
        """
    )
