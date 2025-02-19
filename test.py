import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

# Переменная для хранения текущего состояния
current_mode = "points"  # "points" или "lines"

# Текст, отображающий текущий режим
textObject = OnscreenText(text=f"Current Mode: {current_mode.title()}",
                          pos=(0.0, 0.8), scale=0.07,
                          fg=(1, 1, 1, 1), align=TextNode.ACenter,
                          mayChange=True)

# Функция для переключения между режимами
def set_mode(mode):
    global current_mode
    current_mode = mode
    textObject.setText(f"Current Mode: {current_mode.title()}")

    # Обновляем цвета кнопок
    if current_mode == "points":
        points_button["frameColor"] = (0.3, 0.3, 0.3, 1)
        lines_button["frameColor"] = (0.6, 0.6, 0.6, 1)
    else:
        points_button["frameColor"] = (0.6, 0.6, 0.6, 1)
        lines_button["frameColor"] = (0.3, 0.3, 0.3, 1)

# Создаем кнопки
points_button = DirectButton(
    text="Points",
    scale=0.1, pos=(-0.3, 0, 0),
    frameColor=(0.6, 0.6, 0.6, 1),  # Светлее для выбранного
    command=set_mode,
    extraArgs=["points"]
)

lines_button = DirectButton(
    text="Lines",
    scale=0.1, pos=(0.3, 0, 0),
    frameColor=(0.3, 0.3, 0.3, 1),  # Темнее для невыбранного
    command=set_mode,
    extraArgs=["lines"]
)

# Запуск
base.run()