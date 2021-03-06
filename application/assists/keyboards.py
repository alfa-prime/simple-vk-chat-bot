from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class Keyboards:
    @staticmethod
    def search():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Начать поиск', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def new_search():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Новый поиск', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Инфо', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def main():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Инфо', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Поиск', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def choose_source_user():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Для меня', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Не для меня', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_yes_or_no():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Да', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Нет', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_search_option_with_age():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Ровестники', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Диапазон', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_search_option_without_age():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Диапазон', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_search_option_sex():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Мужчин', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Женщин', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_search_option_relation():
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button('Не женат/Не замужем', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button('В активном поиске', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def ask_search_option_city(city_name):
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_button(f'{city_name}', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Другой', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def process_target(link):
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_openlink_button('Подробнее', link=link)
        keyboard.add_line()
        keyboard.add_button(f'Да', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(f'Нет', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button(f'Не знаю', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(f'Прервать поиск', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    @staticmethod
    def process_chosen(link):
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_openlink_button('Подробнее', link=link)
        keyboard.add_button(f'Дальше', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(f'Убрать из избранного', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button(f'Прервать просмотр', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()
