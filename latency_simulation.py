
%matplotlib inline
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib, collections
from scipy.stats import norm
import imp, os, pickle
import warnings
from matplotlib import collections  as mc
from scipy.stats import poisson
warnings.filterwarnings("ignore")
from scipy.stats import norm
sns.set(style="white")
colors = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]

f = 0.1 #Mining rate
m = 200 #Number of voting chains
log_epsilon = 20 #Confirmation guarantee


# Number of adverserial blocks in private at time t
def adverserial(t, beta, fv):
    x = np.arange(0, 100, 1)
    mu = fv * t * beta / (1 - beta)
    return poisson.pmf(x, mu)


# Probability that a vote with depth k will be removed when adversary has Z_t blocks in private
def p_k_t(k, Z_t, beta):
    ans = 0
    k = int(k)
    for i in range(k):
        ans += Z_t[i] * np.power(beta / (1 - beta), k - i)
    ans += np.sum(Z_t[k:])
    return ans


def runExp(m, log_epsilon, f):
    events = int(2000*log_epsilon)
    beta_array = np.array([0.1, 0.15, 0.2, 0.25, .3, .35, 0.4])
    time_array = np.zeros_like(beta_array)
    f_effective = f/(1.0+2*f) #Forking
    exp_random_v = np.random.exponential(1/(m*f_effective), size=events)
    chain_random_v = np.random.randint(m, size=events)
    #
    #
    #
    for j, beta in enumerate(beta_array):
        time = 0;
        for i, tDiff in enumerate(exp_random_v):
            time += tDiff
            #decide if under attack, pick heaviest chain or fork
            #update block count
    return time_array


beta_array = np.array([0.1, 0.15, 0.2, 0.25, .3, .35, 0.4])
prism_ans = np.zeros_like(beta_array)
# T1: Time taken for a unique proposer block to refer the tx_block
prism_ans += np.power(np.e, 1 * f) / f

# T2: Time taken for a proposer block to get confirmed
no_exp = 5
for i in range(no_exp):
    prism_ans += runExp(m, log_epsilon, f)
prism_ans /= no_exp


exponent = 0.8*(1-2*beta_array)/(1-beta_array)*np.log((1-beta_array)/beta_array)
bitcoin_ans= (log_epsilon+np.log2(150))/(exponent*f)


fig = plt.figure(figsize=(15,7))
ax = fig.add_subplot(111)

bitcoin_ans = bitcoin_ans.astype(int)
prism_ans = prism_ans.astype(int)
plt.plot(beta_array, bitcoin_ans, '-o', lw=3, label="Longest chain")
plt.plot(beta_array, prism_ans, '-o',lw=3, label="Prism")
for i in range(bitcoin_ans.shape[0]):
    ax.annotate(bitcoin_ans[i],xy=(beta_array[i],bitcoin_ans[i]+40), size=25)
    ax.annotate(prism_ans[i],xy=(beta_array[i],prism_ans[i]+40), size=25)
plt.ylabel("Confirmation latency (secs)", size=25)
# plt.xlabel("Beta", size=30)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.title("Time to confirm a block with epsilon = $e$^("+str(-log_epsilon)+") gaurantee m ="+str(m), size=25)
plt.legend(prop={'size': 25})
plt.show()
