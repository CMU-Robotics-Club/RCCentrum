from django.db import models
from crm.models import UpdatedByModel

class VoteableModel(UpdatedByModel):
  """
  Model that can be voted on by upvoting and downvoting.
  """

  up_votes = models.IntegerField(editable=False, default=0)
  down_votes = models.IntegerField(editable=False, default=0)

  @property
  def net_votes(self):
    """
    Ranking by weighting up votes with down votes.
    """

    return self.up_votes + self.down_votes

  @property
  def total_votes(self):
    """
    Ranking by total times voted regardless of whether
    vote was an upvote or downvote.
    """

    return self.up_votes - self.down_votes

  def upvote(self):
    """
    Upvote this instance.
    """

    self.up_votes += 1
    self.save()

  def downvote(self):
    """
    Downvote this instance.
    """

    self.down_votes -= 1
    self.save()

  class Meta:
    abstract = True


class Quote(VoteableModel):

  quote = models.TextField()

  def __str__(self):
    return self.quote
