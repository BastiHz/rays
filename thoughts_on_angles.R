x1 <- c(0, 1)
y1 <- c(0, 0)

angle <- pi / 8
x2 <- c(0, cos(angle))
y2 <- c(0, sin(angle))

x3 <- c(1, 1)
y3 <- c(0, tan(angle))

plot(x1, y1, type = "l", ylim = c(0, 1), asp = 1)
abline(v = 1, lty = 3)
lines(x2, y2, col = "blue")
lines(x2 * 2, y2 * 2, col = "blue", lty = 2)
lines(x3, y3, col = "red")


dy <- seq(0.5, 3, 0.5)
angles <- atan(dy)

plot(x1, y1, type = "l", ylim = c(0, 3), asp = 1)
abline(v = 1, lty = 3)
my_colors <- rainbow(length(dy))
for (i in 1:length(dy)) {
    lines(c(1, 1), c(dy[i] - 0.5, dy[i]), col = my_colors[i])
}
for (a in angles) {
    x2 <- c(0, cos(a))
    y2 <- c(0, sin(a))
    lines(x2, y2, col = "blue")
    lines(x2 * 10, y2 * 10, col = "blue", lty = 2)
}

# Der maximale Winkel hier ist
tail(angles, 1) / pi * 180  # 71.5°
# und das fov ist das Doppelte davon.
# Wenn ich einen fov von 90° will, muss der maximale Winkel +- 45° sein.
max_angle <- 45 * pi / 180  # 45° in Radians
# Maximale vertikale Distanz von der Grundlinie:
tan_max <- tan(max_angle)
# Winkel für 10 Linien:
n <- 10
y <- seq(0, tan_max, length.out = n)
angles <- atan(y)

plot(NA, NA, xlim = c(0, 1), ylim = c(0, 1), asp = 1)
abline(v = 1)
abline(h = y, lty = 3)
for (a in angles) {
    x2 <- c(0, cos(a))
    y2 <- c(0, sin(a))
    lines(x2, y2, col = "blue")
    lines(x2 * 10, y2 * 10, col = "blue", lty = 2)
}

# So oder so ähnlich. Sicherstellen, dass jeder Strahl einen anderen Winkel hat.
# Aber was ist mit der Verzerrung? Die Distanzen sind doch relativ zur Länge der
# Strahlen, oder? Und ich muss es am Schluss mit der Grundlänge normalisieren?
# Dann könnte ich die Strahlen bis zur vertikalen Linie laufen lasse, also mit
# unterschiedlicher Länge, dann löst sich die verzerrung automatisch? Mal
# ausprobieren.
