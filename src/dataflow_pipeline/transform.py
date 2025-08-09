import apache_beam as beam

class FilterErrors(beam.DoFn):
    def process(self, element):
        if len(element) >= 3 and element[2] == '200':  # status_code
            yield element

class AggregateByUser(beam.DoFn):
    def process(self, element):
        try:
            user_id = int(element[1])
            bytes_sent = int(element[4])
            yield (user_id, bytes_sent)
        except (IndexError, ValueError):
            pass

class SumBytes(beam.CombineFn):
    def create_accumulator(self):
        return 0

    def add_input(self, accumulator, input):
        return accumulator + input

    def merge_accumulators(self, accumulators):
        return sum(accumulators)

    def extract_output(self, accumulator):
        return accumulator
