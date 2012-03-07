import pygame, sys
from pygame.locals import *
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

GAME_OVER = False
DECISION = False
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

#Opponent paddle vertically centered on right side
paddle_rect2 = pygame.Rect((SCREEN_WIDTH - 20, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

#Line in the middle
midline = pygame.Rect((SCREEN_WIDTH/2-2, 0), (4, SCREEN_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score1 = 0
score2 = 0
# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse


	if GAME_OVER == True:
		gameovertext = font.render("Game Over.  Press any key to play again", True, (0, 0, 0))
		screen.blit(gameovertext, ((SCREEN_WIDTH / 2), SCREEN_HEIGHT/2 - 200))
		pygame.display.flip()
		while DECISION ==False:
			if (pygame.event.wait().type == KEYDOWN):
				DECISION = True
				score1 = 0
				score2 = 0
				GAME_OVER = False
		DECISION = False
	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
	
	#Tests for other paddle
	if pygame.key.get_pressed()[pygame.K_w] and paddle_rect2.top > 0:
		paddle_rect2.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect2.bottom < SCREEN_HEIGHT:
		paddle_rect2.top += BALL_SPEED
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if ball_rect.right >= SCREEN_WIDTH or ball_rect.left <= 0:
		ball_speed[0] = -ball_speed[0]
	if ball_rect.left <=0:
		score2 += 1
		if score2 >= 11:
			GAME_OVER = True
		ball_speed[0] = 10
		ball_speed[1] = 10
		ball_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
		ball_speed[0] = -ball_speed[0]
	if ball_rect.right >= SCREEN_WIDTH:
		score1 += 1
		if score1 >= 11:
			GAME_OVER = True
		ball_speed[0] = -10
		ball_speed[1] = 10
		ball_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
		ball_speed[0] = -ball_speed[0]
		
	
		
	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect) and ball_speed[0] < 0:
		ball_speed[0] = -ball_speed[0]
		ball_speed[0] += 0.5
		if ball_speed[1] >0:
			ball_speed[1] += 0.5
		else:
			ball_speed[1] -= 0.5
		try:
			sound = pygame.mixer.Sound("fart-3.wav")
		except pygame.error, message:
			print "Cannot load sound: " + sound_name
			raise SystemExit, message
		sound.play()
	if paddle_rect2.colliderect(ball_rect) and ball_speed[0] > 0:
		ball_speed[0] = -ball_speed[0]
		ball_speed[0] -= 0.5
		if ball_speed[1] >0:
			ball_speed[1] += 0.5
		else:
			ball_speed[1] -= 0.5
		try:
			sound = pygame.mixer.Sound("fart-3.wav")
		except pygame.error, message:
			print "Cannot load sound: " + sound_name
			raise SystemExit, message
		sound.play()
	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddles, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect2) # Opponent paddle
	pygame.draw.rect(screen, (255,0,0), midline) #mid line
	
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text1 = font.render(str(score1), True, (0, 0, 0))
	score_text2 = font.render(str(score2), True, (0, 0, 0))
	screen.blit(score_text1, ((SCREEN_WIDTH / 4) - font.size(str(score1))[0] / 2, 5)) # The score for you
	screen.blit(score_text2, ((SCREEN_WIDTH / 4)*3 - font.size(str(score2))[0] / 2, 5)) # The score for opponent
	
	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
