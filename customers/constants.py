POLICY_DURATION_DAYS = 365


class PolicyStateChoices:
    NEW = 'new'
    QUOTED = 'quoted'
    ACCEPTED = 'accepted'
    ACTIVE = 'active'

    CHOICES = (
        (NEW, 'New'),
        (QUOTED, 'Quoted'),
        (ACCEPTED, 'Accepted'),
        (ACTIVE, 'Active'),
    )
