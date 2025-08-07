"""
Точка входа в игру
"""

from game import Game

def main():
    """
    Главная функция игры
    """
    print("🎮 Starting Platformer 'Save the Heroes!'")
    print("=" * 50)
    print("📖 Story:")
    print("   - Choose one of 3 heroines")
    print("   - Complete 3 levels")
    print("   - Defeat the hippo boss")
    print("   - Save 3 male heroes!")
    print("=" * 50)
    print("🎮 Controls:")
    print("   - Arrow keys or WASD - movement")
    print("   - Space - jump")
    print("   - ESC - exit to menu")
    print("=" * 50)
    print("🎯 Objective:")
    print("   - Jump on enemies from above to defeat them")
    print("   - Avoid falling into pits")
    print("   - Defeat the boss by jumping on him")
    print("=" * 50)
    
    # Создаем и запускаем игру
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 