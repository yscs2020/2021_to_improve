{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "###########################################\n",
    "# Suppress matplotlib user warnings\n",
    "# Necessary for newer version of matplotlib\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\", category = UserWarning, module = \"matplotlib\")\n",
    "#\n",
    "# Display inline matplotlib plots with IPython\n",
    "from IPython import get_ipython\n",
    "get_ipython().run_line_magic('matplotlib', 'inline')\n",
    "###########################################\n",
    "\n",
    "import matplotlib.pyplot as pl\n",
    "import numpy as np\n",
    "from sklearn.model_selection import learning_curve, validation_curve\n",
    "from sklearn.tree import DecisionTreeRegressor\n",
    "from sklearn.model_selection import ShuffleSplit, train_test_split\n",
    "\n",
    "\n",
    "def ModelLearning(X, y):\n",
    "    \"\"\" Calculates the performance of several models with varying sizes of training data.\n",
    "        The learning and validation scores for each model are then plotted. \"\"\"\n",
    "    \n",
    "    # Create 10 cross-validation sets for training and testing\n",
    "    cv = ShuffleSplit(n_splits = 10, test_size = 0.2, random_state = 0)\n",
    "\n",
    "\n",
    "    # Generate the training set sizes increasing by 50\n",
    "    train_sizes = np.rint(np.linspace(1, X.shape[0]*0.8 - 1, 9)).astype(int)\n",
    "\n",
    "    # Create the figure window\n",
    "    fig = pl.figure(figsize=(10,7))\n",
    "\n",
    "    # Create three different models based on max_depth\n",
    "    for k, depth in enumerate([1,3,6,10]):\n",
    "        \n",
    "        # Create a Decision tree regressor at max_depth = depth\n",
    "        regressor = DecisionTreeRegressor(max_depth = depth)\n",
    "\n",
    "        # Calculate the training and testing scores\n",
    "        sizes, train_scores, valid_scores = learning_curve(regressor, X, y, \\\n",
    "            cv = cv, train_sizes = train_sizes, scoring = 'r2')\n",
    "        \n",
    "        # Find the mean and standard deviation for smoothing\n",
    "        train_std = np.std(train_scores, axis = 1)\n",
    "        train_mean = np.mean(train_scores, axis = 1)\n",
    "        valid_std = np.std(valid_scores, axis = 1)\n",
    "        valid_mean = np.mean(valid_scores, axis = 1)\n",
    "#         print train_mean\n",
    "#         print train_scores\n",
    "\n",
    "        # Subplot the learning curve \n",
    "        ax = fig.add_subplot(2, 2, k+1)\n",
    "        ax.plot(sizes, train_mean, 'o-', color = 'r', label = 'Training Score')\n",
    "        ax.plot(sizes, valid_mean, 'o-', color = 'g', label = 'Validation Score')\n",
    "        ax.fill_between(sizes, train_mean - train_std, \\\n",
    "            train_mean + train_std, alpha = 0.15, color = 'r')\n",
    "        ax.fill_between(sizes, valid_mean - valid_std, \\\n",
    "            valid_mean + valid_std, alpha = 0.15, color = 'g')\n",
    "        \n",
    "        # Labels\n",
    "        ax.set_title('max_depth = %s'%(depth))\n",
    "        ax.set_xlabel('Number of Training Points')\n",
    "        ax.set_ylabel('r2_score')\n",
    "        ax.set_xlim([0, X.shape[0]*0.8])\n",
    "        ax.set_ylim([-0.05, 1.05])\n",
    "    \n",
    "    # Visual aesthetics\n",
    "    ax.legend(bbox_to_anchor=(1.05, 2.05), loc='lower left', borderaxespad = 0.)\n",
    "    fig.suptitle('Decision Tree Regressor Learning Performances', fontsize = 16, y = 1.03)\n",
    "    fig.tight_layout()\n",
    "    fig.show()\n",
    "\n",
    "\n",
    "def ModelComplexity(X, y):\n",
    "    \"\"\" Calculates the performance of the model as model complexity increases.\n",
    "        The learning and validation errors rates are then plotted. \"\"\"\n",
    "    \n",
    "    # Create 10 cross-validation sets for training and testing\n",
    "    cv = ShuffleSplit(n_splits = 10, test_size = 0.2, random_state = 0)\n",
    "\n",
    "    # Vary the max_depth parameter from 1 to 10\n",
    "    max_depth = np.arange(1,11)\n",
    "\n",
    "    # Calculate the training and testing scores\n",
    "    train_scores, valid_scores = validation_curve(DecisionTreeRegressor(), X, y, \\\n",
    "        param_name = \"max_depth\", param_range = max_depth, cv = cv, scoring = 'r2')\n",
    "\n",
    "    # Find the mean and standard deviation for smoothing\n",
    "    train_mean = np.mean(train_scores, axis=1)\n",
    "    train_std = np.std(train_scores, axis=1)\n",
    "    valid_mean = np.mean(valid_scores, axis=1)\n",
    "    valid_std = np.std(valid_scores, axis=1)\n",
    "\n",
    "    # Plot the validation curve\n",
    "    pl.figure(figsize=(7, 5))\n",
    "    pl.title('Decision Tree Regressor Complexity Performance')\n",
    "    pl.plot(max_depth, train_mean, 'o-', color = 'r', label = 'Training Score')\n",
    "    pl.plot(max_depth, valid_mean, 'o-', color = 'g', label = 'Validation Score')\n",
    "    pl.fill_between(max_depth, train_mean - train_std, \\\n",
    "        train_mean + train_std, alpha = 0.15, color = 'r')\n",
    "    pl.fill_between(max_depth, valid_mean - valid_std, \\\n",
    "        valid_mean + valid_std, alpha = 0.15, color = 'g')\n",
    "    \n",
    "    # Visual aesthetics\n",
    "    pl.legend(loc = 'lower right')\n",
    "    pl.xlabel('Maximum Depth')\n",
    "    pl.ylabel('r2_score')\n",
    "    pl.ylim([-0.05,1.05])\n",
    "    pl.show()\n",
    "\n",
    "\n",
    "def PredictTrials(X, y, fitter, data):\n",
    "    \"\"\" Performs trials of fitting and predicting data. \"\"\"\n",
    "\n",
    "    # Store the predicted prices\n",
    "    prices = []\n",
    "\n",
    "    for k in range(10):\n",
    "        # Split the data\n",
    "        X_train, X_test, y_train, y_test = train_test_split(X, y, \\\n",
    "            test_size = 0.2, random_state = k)\n",
    "        \n",
    "        # Fit the data\n",
    "        reg = fitter(X_train, y_train)\n",
    "        \n",
    "        # Make a prediction\n",
    "        pred = reg.predict([data[0]])[0]\n",
    "        prices.append(pred)\n",
    "        \n",
    "        # Result\n",
    "        print(\"Trial {}: ${:,.2f}\".format(k+1, pred))\n",
    "\n",
    "    # Display price range\n",
    "    print(\"\\nRange in prices: ${:,.2f}\".format(max(prices) - min(prices)))\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
