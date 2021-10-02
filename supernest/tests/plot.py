import matplotlib.pyplot as plt
from anesthetic import NestedSamples

def main():
    control = NestedSamples(root="chains/control")
    proposal = NestedSamples(root="chains/proposal")
    super = NestedSamples(root="chains/super")
    tuned_super = NestedSamples(root="chains/tuned_super")

    thetas= ["theta0", "theta1", "theta2", "theta3"]

    fig, ax = control.plot_2d(thetas)
    proposal.plot_2d(ax)
    super.plot_2d(ax)
    plt.show()


if __name__ == '__main__':
    main()
