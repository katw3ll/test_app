from VideoAnalyser import VideoAnalyser


def analyze(path):
    analyzer = VideoAnalyser(path)
    analyzer.analyze()
    return analyzer.get_all_timestaps()