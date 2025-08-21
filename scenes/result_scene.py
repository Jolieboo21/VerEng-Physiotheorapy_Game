import pygame
from ui.button import Button

# Exercise mapping với tên tiếng Anh đẹp
exercise_mapping = {
     'knee_raise': 'Knee Raise',
    'forward_bend': 'Forward Bend',
    'arms_crossed': 'Arms Crossed',
    'arms_legs_combined': 'Arms & Legs Combined',
    'leg_extension': 'Leg Extension',
    'arms_raised': 'Arms Raised',
    'arms_sideways': 'Arms Sideways',
    'arms_front_chest': 'Arms Front Chest',
    'chest_exercise': 'Chest Exercise',
    'arms_rotation': 'Arms Rotation'
}

# Level mapping tiếng Anh
level_mapping = {
    'Hand Exercise': 'Arms Exercises',
    'Leg Exercise': 'Legs Exercises',
    'Level 1': 'Warm-up',
    'Level 2': 'Flexibility',
    'Level 3': 'Mastery'
}

class ResultScene:
    def __init__(self, screen, player_data, all_players):
        self.screen = screen
        self.screen_width = 1280
        self.screen_height = 720
        self.font = pygame.font.Font("assets/fonts/K2D-Light.ttf", 20)
        self.bold_font = pygame.font.Font("assets/fonts/K2D-Bold.ttf", 20)
        self.player_data = player_data
        self.stop_button = Button("assets/images/stop_button.png", self.screen_width // 2 - 75 - 150, 680, width=150, height=75)
        self.next_button = Button("assets/images/continue_button.png", self.screen_width // 2 + 75 + 150, 680, width=150, height=75)
        self._is_done = False
        self.next_scene = None
        self.all_players = all_players
        self.background = pygame.image.load("assets/images/result_bg.png").convert()
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._is_done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.stop_button.is_clicked(mouse_pos):
                self._is_done = True
                self.next_scene = None
            elif self.next_button.is_clicked(mouse_pos):
                self._is_done = True
                self.next_scene = "LevelSelectScene"

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Player info tiếng Anh
        name_text = self.bold_font.render(f"Player: {self.player_data.name}", True, (0, 0, 0))
        total_score_text = self.bold_font.render(f"Total Score: {self.player_data.total_score}", True, (0, 0, 0))
        total_time_text = self.bold_font.render(f"Total Time: {self.player_data.total_time:.2f}s", True, (0, 0, 0))
        level_text = self.bold_font.render(f"Level: {level_mapping.get(self.player_data.level, self.player_data.level)}", True, (0, 0, 0))

        self.screen.blit(name_text, (50, 470))
        self.screen.blit(total_score_text, (50, 500))
        self.screen.blit(total_time_text, (50, 530))
        self.screen.blit(level_text, (50, 560))

        # Chart settings
        chart_x, chart_y, chart_width, chart_height = 70, 50, 1000, 300
        num_exercises = len(self.player_data.exercise_names)
        bar_width = chart_width / (num_exercises * 2 + 1) if num_exercises > 0 else 10
        max_score = max(self.player_data.exercise_scores) if self.player_data.exercise_scores else 1
        max_time = max(self.player_data.exercise_times) if self.player_data.exercise_times else 1

        for i, (name, score, time) in enumerate(zip(self.player_data.exercise_names, self.player_data.exercise_scores, self.player_data.exercise_times)):
            # Lấy tên tiếng Anh từ mapping
            display_name = exercise_mapping.get(name, name)

            # Vẽ điểm
            bar_height_score = (score / max_score) * chart_height
            bar_x_score = chart_x + (chart_width - (num_exercises * 2 * bar_width)) / 2 + i * 2 * bar_width
            pygame.draw.rect(self.screen, (255, 165, 0), (bar_x_score, chart_y + chart_height - bar_height_score, bar_width - 5, bar_height_score))
            self.screen.blit(self.font.render(f"{score}", True, (0, 0, 0)), (bar_x_score, chart_y + chart_height - bar_height_score - 30))

            # Vẽ thời gian
            bar_height_time = (time / max_time) * chart_height
            bar_x_time = bar_x_score + bar_width
            pygame.draw.rect(self.screen, (255, 200, 100), (bar_x_time, chart_y + chart_height - bar_height_time, bar_width - 5, bar_height_time))
            self.screen.blit(self.font.render(f"{time:.2f}", True, (0, 0, 0)), (bar_x_time, chart_y + chart_height - bar_height_time - 30))

            # Vẽ tên bài tập tiếng Anh
            name_text = self.font.render(display_name, True, (0, 0, 0))
            self.screen.blit(name_text, (bar_x_score + bar_width / 2 - name_text.get_width() / 2, chart_y + chart_height + 15))

        # Chú thích (legend)
        legend_x = chart_x + chart_width + 20
        pygame.draw.rect(self.screen, (255, 165, 0), (legend_x - 30, chart_y, 20, 20))  # Score
        pygame.draw.rect(self.screen, (255, 200, 100), (legend_x - 30, chart_y + 40, 20, 20))  # Time
        self.screen.blit(self.font.render("Score", True, (0, 0, 0)), (legend_x, chart_y))
        self.screen.blit(self.font.render("Time", True, (0, 0, 0)), (legend_x, chart_y + 40))

        # Bài tập tốt nhất và cần cải thiện
        if self.player_data.exercise_scores and self.player_data.exercise_times and len(self.player_data.exercise_scores) > 1:
            best_index = max(range(len(self.player_data.exercise_scores)), key=lambda i: (self.player_data.exercise_scores[i], -self.player_data.exercise_times[i]))
            remaining_indices = [i for i in range(len(self.player_data.exercise_scores)) if i != best_index]
            worst_index = min(remaining_indices, key=lambda i: (self.player_data.exercise_scores[i], -self.player_data.exercise_times[i]), default=best_index) if remaining_indices else best_index

            best_name = exercise_mapping.get(self.player_data.exercise_names[best_index], self.player_data.exercise_names[best_index])
            worst_name = exercise_mapping.get(self.player_data.exercise_names[worst_index], self.player_data.exercise_names[worst_index])

            best_text = self.bold_font.render(f"Best Exercise: {best_name}", True, (0, 0, 139))
            worst_text = self.bold_font.render(f"Needs Improvement: {worst_name}", True, (0, 0, 139))
            self.screen.blit(best_text, (50, 590))
            self.screen.blit(worst_text, (50, 620))
        else:
            no_data_text = self.font.render("Not enough data to determine best/needs improvement", True, (255, 0, 0))
            self.screen.blit(no_data_text, (50, 620))

        # Leaderboard (bảng xếp hạng)
        if self.player_data.level and self.all_players:
            current_level_players = [p for p in self.all_players if p.level == self.player_data.level]
            if current_level_players:
                current_level_players.sort(key=lambda x: (x.total_score, -x.total_time), reverse=True)
                player_index = next((i for i, p in enumerate(current_level_players) if p.name == self.player_data.name), None)

                table_x = 720
                table_y = 530
                cell_widths = [60, 200, 100, 120]
                cell_height = 30
                line_spacing = 10

                # Tiêu đề tiếng Anh
                headers = ["Rank", "Name", "Score", "Time"]
                header_x = table_x
                header_y = table_y - cell_height - line_spacing
                for col_idx, header in enumerate(headers):
                    col_width = cell_widths[col_idx]
                    header_surface = self.font.render(header, True, (0, 0, 0))
                    text_rect = header_surface.get_rect(center=(header_x + col_width // 2, header_y + cell_height // 2))
                    self.screen.blit(header_surface, text_rect)
                    header_x += col_width

                display_rows = []
                rank1 = current_level_players[0]
                display_rows.append(("1", rank1.name, rank1.total_score, f"{rank1.total_time:.2f}s"))

                if player_index is not None and player_index > 0:
                    above_player = current_level_players[player_index - 1]
                    display_rows.append((f"{player_index}", above_player.name, above_player.total_score, f"{above_player.total_time:.2f}s"))
                else:
                    display_rows.append(("-", "No player above", "", ""))

                current_rank = player_index + 1 if player_index is not None else len(current_level_players) + 1
                display_rows.append((f"{current_rank}", self.player_data.name, self.player_data.total_score, f"{self.player_data.total_time:.2f}s"))

                for row_idx, row_data in enumerate(display_rows):
                    x = table_x
                    y = table_y + row_idx * (cell_height + line_spacing)
                    for col_idx, cell in enumerate(row_data):
                        col_width = cell_widths[col_idx]
                        color = (0, 0, 200) if row_idx == 2 else (0, 0, 0)
                        cell_surface = self.font.render(str(cell), True, color)
                        text_rect = cell_surface.get_rect(center=(x + col_width // 2, y + cell_height // 2))
                        self.screen.blit(cell_surface, text_rect)
                        x += col_width

        self.stop_button.draw(self.screen)
        self.next_button.draw(self.screen)

    def is_done(self):
        return self._is_done

    def get_next_scene(self):
        return self.next_scene
