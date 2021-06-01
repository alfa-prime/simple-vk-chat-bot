from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class Keyboards:
    @staticmethod
    def search():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

    @staticmethod
    def new_search():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Новый поиск', color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

    @staticmethod
    def main():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Инфо', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

    @staticmethod
    def choose_search_option_by_age():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Ровестники', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Диапазон', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def choose_search_option_by_sex():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Мужчин', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Женщин', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Неважно', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def choose_search_option_by_city():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Родной город', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Указать другой', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def hide():
        return VkKeyboard.get_empty_keyboard()
