from sb3_contrib import TQC
from stable_baselines3 import PPO
import gym
import numpy as np

env = gym.make("gym_rocketlander:rocketlander-v0")
model = TQC.load("/home/hanzopgp/projects/MasterArtificialIntelligencePTs/S3/RLD/TME_bonus/tqc_rocketlander_test3.zip", env=env, device="cpu")
# BEST IS 13, 15, 4

# env = gym.make("LunarLander-v2")
# model = PPO.load("/home/hanzopgp/projects/MasterArtificialIntelligencePTs/S3/RLD/TME_bonus/agents/LunarLander-v2ppocanitrot_dubreuil_sb3 (1).zip", env=env, device="cpu")
n_envs = 1

obs = env.reset()

# Deterministic by default except for atari games
stochastic = False
deterministic = not stochastic

episode_reward = 0.0
episode_rewards, episode_lengths = [], []
ep_len = 0
# For HER, monitor success rate
successes = []
lstm_states = None
episode_start = np.ones((n_envs,), dtype=bool)

generator = range(1000)

try:
	for _ in generator:
		action, lstm_states = model.predict(
			obs,
			state=lstm_states,
			episode_start=episode_start,
			deterministic=deterministic,
		)
		obs, reward, done, infos = env.step(action)

		episode_start = done

		env.render("human")

		episode_reward += reward
		ep_len += 1

		if n_envs == 1:

			if done:
				# NOTE: for env using VecNormalize, the mean reward
				# is a normalized reward when `--norm_reward` flag is passed
				print(f"Episode Reward: {episode_reward:.2f}")
				print("Episode Length", ep_len)
				episode_rewards.append(episode_reward)
				episode_lengths.append(ep_len)
				episode_reward = 0.0
				ep_len = 0

			# Reset also when the goal is achieved when using HER
			if infos.get("is_success") is not None:
				print("Success?", infos[0].get("is_success", False))
				successes.append(infos[0].get("is_success", False))
				episode_reward, ep_len = 0.0, 0

except KeyboardInterrupt:
	pass

if len(successes) > 0:
	print(f"Success rate: {100 * np.mean(successes):.2f}%")

if len(episode_rewards) > 0:
	print(f"{len(episode_rewards)} Episodes")
	print(f"Mean reward: {np.mean(episode_rewards):.2f} +/- {np.std(episode_rewards):.2f}")

if len(episode_lengths) > 0:
	print(f"Mean episode length: {np.mean(episode_lengths):.2f} +/- {np.std(episode_lengths):.2f}")

env.close()
