# Per funzionare devo sempre abilitare prima una libreria con il seguente comando
# export LD_PRELOAD=/usr/lib64/libstdc++.so.6
#
# non puo' essere fatto direttamente dal codice python
import gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from MazeEnv import MazeEnv


def main():
    # validation
    env = MazeEnv(10, 10)
    # check_env(env, warn=True)

    # stato iniziale del labirinto
    obs = env.reset()
    env.render()
    input("Premi [Enter] per continuare")

    print(f"Observ Space:\n{env.observation_space}")
    print(f"Action Space:\n{env.action_space}")
    print(f"Action Sample:\n{env.action_space.sample()}")
    print(f"Observ Sample:\n{env.observation_space.sample()}")
    print("")

    steps = int(2e5)
    model = DQN('MlpPolicy', env, verbose=0)

    while True:
        print("Training ...")
        model.learn(total_timesteps=steps)
        print("Done !")
        print("")
        print("Simulating ...")
        obs = env.reset()
        for i in range(100):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            if done:
                obs = env.reset()
                env.close()
                return

        env.close()

    # exit()

    """
    n_steps = 20
    for step in range(n_steps):
        print("Step {}".format(step + 1))
        obs, reward, done, info = env.step(env.actions["down"])
        print('obs=', obs, 'reward=', reward, 'done=', done)
        env.render()
        if done:
            print("Goal reached!", "reward=", reward)
            break
    """
    """env = gym.make("CartPole-v1")

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)

    obs = env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
          obs = env.reset()

    env.close()"""


if __name__ == "__main__":
    # check se la libreria necessaria al rendering e' stata importata
    try:
        from pyglet.gl import ContextException
    except Exception:
        print("Potresti non aver abilitato la libreria GLIBCXX_3.4.29.")
        print("Usa il seguente comando per farlo e poi riavvia lo script:")
        print("")
        print("\texport LD_PRELOAD=/usr/lib64/libstdc++.so.6")
        exit(1)

    # esecuzione del main
    main()
