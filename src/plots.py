def plot_cm(ax, estimator, X_test, y_test):
    
from sklearn.metrics import plot_confusion_matrix


disp = plot_confusion_matrix(classifier, X_test, y_test,
                            display_labels=class_names,
                            cmap=plt.cm.Blues,
                            normalize=normalize)
disp.ax_.set_title(title)
print(title)
print(disp.confusion_matrix)

plt.show()