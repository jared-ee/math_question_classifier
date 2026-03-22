def evaluate(predictions, ground_truths):
    total = len(predictions)

    levels = ["strand", "subStrand", "topic", "learningOutcome", "loId"]

    correct_counts = {level: 0 for level in levels}

    for pred, gt in zip(predictions, ground_truths):
        for level in levels:
            if pred[level] == gt[level]:
                correct_counts[level] += 1

    accuracy = {
        level: correct_counts[level] / total
        for level in levels
    }

    return accuracy