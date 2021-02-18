import sys
from tweepy.streaming import StreamListener


class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener,self).__init__()
        self.output_file = output_file
    def on_status(self, status):
        print('new tweet:')
        print(status.text + '\n')
        print(status.text, file=self.output_file, flush=True)
    def on_error(self, status_code):
        print(status_code)
        return False


if __name__ == "__main__":
    # calling main function
    main()

