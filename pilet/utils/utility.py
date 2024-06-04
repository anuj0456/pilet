from pilet.static import input_prompt


class Utility:
    @staticmethod
    def get_choice_str(choices):
        choices_str = "\n\n".join(
            [f"{idx + 1}. {c}" for idx, c in enumerate(choices)]
        )
        return choices_str

    @staticmethod
    def router_prompt(choices):
        router_prompt = input_prompt.partial_format(
            num_choices=len(choices),
            max_outputs=len(choices),
        )
        return router_prompt
