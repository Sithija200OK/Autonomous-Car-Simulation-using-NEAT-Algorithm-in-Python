import pygame
import neat
from game import game_loop
from car import Car

# Define the fitness evaluation function
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        car = Car()

        # Set up the neural network for each genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Run the simulation for each genome
        sensor_data = []
        for _ in range(500):  # Run for 500 time steps
            sensors, sensor_info = car.get_sensor_data(car.rect, car.angle)

            # Prepare input data for the neural network
            sensor_data = [sensor["distance"] for sensor in sensor_info]

            # Get control signals from the network (steering, throttle, brake)
            output = net.activate(sensor_data)
            steering, throttle, brake = output[0], output[1], output[2]

            # Update the car state based on network outputs
            car.update(steering, throttle, brake)

            # Increase fitness based on the distance traveled
            genome.fitness += car.velocity

# Run the NEAT algorithm
def run():
    config_path = 'config.txt'
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create population
    population = neat.Population(config)

    # Add reporters to track progress
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    # Run for 50 generations
    population.run(eval_genomes, 50)

# Start the NEAT algorithm
if __name__ == '__main__':
    run()
