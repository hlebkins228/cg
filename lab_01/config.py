points_size = 7
plot_fontsize = 7

set_1_rgb_color = (255, 58, 54)
set_2_rgb_color = (0, 213, 85)

points_color_1 = [i / 255 for i in set_1_rgb_color]
points_color_2 = [i / 255 for i in set_2_rgb_color]

border_color_1 = '(' + ", ".join(list(map(str, set_1_rgb_color))) + ')'
border_color_2 = '(' + ", ".join(list(map(str, set_2_rgb_color))) + ')'

columns_count = 2

cord_regexp = "^[-+]?[0-9]*[.]?[0-9]+(?:[eE][-+]?[0-9]+)?$"

calc_accuracy = 5

eps = 10 ** -3
steps_count = 100_000       # old
