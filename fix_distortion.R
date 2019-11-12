# I want to get a better understanding of why the view in my pygame app is
# distorted. Maybe this R script will help.

# Die weißen Lücken sind artefakte, weil die Breite des Plot-Fensters nicht zur
# Anzahl der Linien passt. Einfach ignorieren.

# Also ich kann hier keine Verzerrung mehr sehen. Habe ich vielleicht in Python
# einen Fehler gemacht? Ich muss mal die Zahlen alle vergleichen.


camera_position <- c(0, 20)
camera_angle <- pi / 2  # straight upwards
fov <- pi / 2  # 90 degrees
screen_width <- 400
screen_height <- 400

walls <- data.frame(
    x1 = c(-100, -200),
    y1 = c(300, 100),
    x2 = c(200, -100),
    y2 = c(200, 200)
)
# Wand orthogonal zur Kamera:
# walls <- data.frame(
#     x1 = -200,
#     y1 = 300,
#     x2 = 200,
#     y2 = 300
# )

rays <- data.frame(
    screen_x = seq(-screen_width/2, length.out = screen_width),
    screen_y1 = NA,
    screen_y2 = NA,
    x1 = camera_position[1],
    y1 = camera_position[2],
    relative_angle = -atan(
        seq(-tan(fov / 2), tan(fov / 2), length.out = screen_width)
    ),
    intersect_x = NA,
    intersect_y = NA,
    distance = NA,
    hit = FALSE
)
rays$angle <- rays$relative_angle + camera_angle
rays$x2 <- rays$x1 + cos(rays$angle)
rays$y2 <- rays$y1 + sin(rays$angle)

for (i in 1:nrow(rays)) {
    ray <- rays[i, ]
    min_distance <- Inf
    for (j in 1:nrow(walls)) {
        # maybe replace this loop with apply()
        w <- walls[j, ]
        denominator <- ((w$x1 - w$x2) * (ray$y1 - ray$y2)
                        - (w$y1 - w$y2) * (ray$x1 - ray$x2))
        if (denominator == 0) {
            next
        }
        t <- (((w$x1 - ray$x1) * (ray$y1 - ray$y2)
              - (w$y1 - ray$y1) * (ray$x1 - ray$x2)) / denominator)
        if (t < 0 || t > 1) {
            next
        }
        u <- -((w$x1 - w$x2) * (w$y1 - ray$y1)
              - (w$y1 - w$y2) * (w$x1 - ray$x1)) / denominator
        if (u <= 0 || u >= min_distance) {
            next
        }
        min_distance <- u
        intersect_x <- w$x1 + t * (w$x2 - w$x1)
        intersect_y <- w$y1 + t * (w$y2 - w$y1)
    }
    if (min_distance < Inf) {
        rays$intersect_x[i] <- intersect_x
        rays$intersect_y[i] <- intersect_y
        distance <- min_distance * cos(rays$relative_angle[i])
        rays$distance[i] <- distance
        rays$hit[i] <- TRUE
        h <- screen_height / distance * 50
        # h <-
        rays$screen_y1[i] <- (screen_height - h) / 2
        rays$screen_y2[i] <- (screen_height + h) / 2
    }
}
rays$color <- ifelse(rays$hit, "yellow", NA)


par(mfrow = c(1, 2), xaxs = "i", yaxs = "i", ann = FALSE, pty = "s",
    mar = c(2, 1, 0, 0)+0.1, las = 1)

plot(NA, NA, xlim = range(rays$screen_x), ylim = c(0, screen_height))
segments(rays$x1, rays$y1, rays$intersect_x, rays$intersect_y, rays$color)
for (i in 1:nrow(walls)) {
    segments(walls$x1[i], walls$y1[i], walls$x2[i], walls$y2[i])
}
# show field of view:
i <- c(1, nrow(rays))
segments(
    rays$x1[i],
    rays$y1[i],
    # Die Endpunkte zum Ursprung schieben, verlängern, dann zurück schieben.
    # Ansonsten stimmen die Winkel nicht mehr.
    (rays$x2[i] - rays$x1[i]) * 1000 + rays$x1[i],
    (rays$y2[i] - rays$y1[i]) * 1000 + rays$y1[i],
    col = "orange"
)

plot(NA, NA, xlim = range(rays$screen_x), ylim = c(1, screen_height))
segments(rays$screen_x, rays$screen_y1, y1 = rays$screen_y2)


# Also an der Verteilung der Winkel liegt es nicht. Das habe ich mit der
# orthogonalen Wand überprüft.
