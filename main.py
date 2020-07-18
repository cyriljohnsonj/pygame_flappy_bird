import os
import neat
# import pickle
import pygame

from models.bird import Bird
from models.pipe import Pipe
from models.ground import Ground
from utils.game_utils import load_pygame_image


pygame.font.init()
pygame.display.set_caption("Flappy Bird")
STAT_FONT = pygame.font.SysFont("comicsans", 50)
WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730
BG_IMG = load_pygame_image("bg.png")
gen = 0


def draw_window(win, birds, pipes, ground, score, gen, pipe_ind):
    if gen == 0:
        gen = 1
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    ground.draw(win)
    for bird in birds:
        bird.draw(win)

    # Score
    score_label = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # Generations
    gen_label = STAT_FONT.render(f"Generations: {gen}", 1, (255, 255, 255))
    win.blit(gen_label, (10, 10))

    # Alive
    alive_label = STAT_FONT.render(f"Alive: {len(birds)}", 1, (255, 255, 255))
    win.blit(alive_label, (10, 50))

    pygame.display.update()


def main(genomes, config):
    global gen
    gen += 1
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    birds = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    pipes = [Pipe(700)]
    ground = Ground(FLOOR)
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            # Determine whether to use the first or second
            if len(pipes) > 1 and birds[0].x > \
                    pipes[0].x + pipes[0].PIPE_TOP.get_width():
                # Pipe on the screen for neural network input
                pipe_ind = 1

        # Give each bird a fitness of 0.1 for each frame it stays alive
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location
            # and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate(
                (
                    bird.y, abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom)
                )
            )

            # We use a tanh activation function so result will be
            # between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                bird.jump()

        ground.move()

        residue = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # Check for collisions
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                residue.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # Add this line to give more reward for passing pipe
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(700))

        for res in residue:
            pipes.remove(res)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(win, birds, pipes, ground, score, gen, pipe_ind)

        # Break when the score is large enough to extract the model
        # if score > 20:
        #     pickle.dump(nets[0], open("best.pickle", "wb"))
        #     break


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.ini")
    run(config_path)
