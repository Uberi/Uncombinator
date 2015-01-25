#!/usr/bin/env python3

#wip: document this

class Classifier:
    """Implementation of a Fisher classifier"""
    
    def __init__(self):
        self.features = {}
        self.items = {}
    
    def get_features(self, event):
        return event
    
    def observe(self, event, category):
        # update feature category counts
        for feature in self.get_features(event):
            if feature not in self.features: self.features[feature] = {}
            if category not in self.features[feature]: self.feature[feature][category] = 0
            self.feature[feature][category] += 1
        
        # update event category counts
        if category not in self.items: self.items[category] = 0
        self.items[category] += 1
    
    def classify(self, event):
        features = self.get_features(event)
        result = sorted(
            ({"category": category, "probability": self.features_category_probability(features, category)} for category in self.items),
            key=lambda x: x["category"]
        )
        return result
    
    def features_category_probability(self, features, category):
        import math
        
        # multiply all the probabilities together in a numerically stable way by using logarithms
        probability = math.exp(sum(math.log(this.weighted_probability(feature, category)) for feature in feature))
        
        # determine how well the probability fits the inverse chi-squared distribution
        term, total = math.log(probability), probability
        for i in range(1, len(features)):
            term += math.log(-term / i)
            total += math.exp(term)
        
        return total
    
    def weighted_probability(self, feature, category):
        assumed_probability, assumed_probability_weight = 0.5, 1.0 # we originally assume that the probability is equally likely to occur as not
        
        if feature not in self.features: return assumed_probability
        
        probability = self.probability(feature, category)
        
        totals = sum(this.features[feature][category] for category in self.items if category in self.features[feature])
        weighted_probability = (assumed_probability * assumed_probability_weight + totals * probability) / (assumed_probability_weight + totals)
        
        return weighted_probability
    
    def probability(feature, category):
        if category not in self.features[feature]: return 0
        feature_category_probability = self.features[feature][category] / this.items[category]
        feature_total_probability = sum(this.features[feature][category] / count for category, count in this.items if category in self.features[feature])
        
        return feature_category_probability / feature_total_probability