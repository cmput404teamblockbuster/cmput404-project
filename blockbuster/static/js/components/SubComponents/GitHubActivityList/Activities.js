
module.exports = {
    mapEventToFunction:function (index) {
        const ActivityArray = [this.CommitCommentEvent, this.CreateEvent,this.DeleteEvent,this.DeploymentEvent,
            this.DeploymentStatusEvent,this.DownloadEvent,this.FollowEvent,this.ForkEvent,this.ForkApplyEvent,this.GistEvent,this.GollumEvent,
            this.IssueCommentEvent,this.IssuesEvent,this.LabelEvent,this.MemberEvent,this.MembershipEvent,this.MilestoneEvent,
            this.OrganizationEvent, this.OrgBlockEvent,this.PageBuildEvent,this.ProjectCardEvent,this.ProjectColumnEvent,this.ProjectEvent,
            this.PublicEvent,this.PullRequestEvent, this.PullRequestReviewEvent,this.PullRequestReviewCommentEvent,this.PushEvent,
            this.ReleaseEvent,this.RepositoryEvent,this.StatusEvent, this.TeamEvent,this.TeamAddEvent,this.WatchEvent
        ];
        return ActivityArray[index]
    },

    CommitCommentEvent: function (data) {

    },
    CreateEvent:function (data) {

    },
    DeleteEvent:function (data) {

    },
    DeploymentEvent:function (data) {

    },
    DeploymentStatusEvent:function (data) {

    },
    DownloadEvent:function (data) {

    },
    FollowEvent:function (data) {

    },
    ForkEvent:function (data) {

    },
    ForkApplyEvent: function (data) {

    },
    GistEvent: function (data) {

    },
    GollumEvent: function (data) {

    },
    IssueCommentEvent: function (data) {

    },
    IssuesEvent: function (data) {

    },
    LabelEvent: function (data) {

    },
    MemberEvent: function (data) {

    },
    MembershipEvent: function (data) {

    },
    MilestoneEvent: function (data) {

    },
    OrganizationEvent: function (data) {

    },
    OrgBlockEvent: function (data) {

    },
    PageBuildEvent: function (data) {

    },
    ProjectCardEvent: function (data) {

    },
    ProjectColumnEvent: function (data) {

    },
    ProjectEvent: function (data) {

    },
    PublicEvent: function (data) {

    },
    PullRequestEvent: function (data) {

    },
    PullRequestReviewEvent: function (data) {

    },
    PullRequestReviewCommentEvent: function (data) {

    },
    PushEvent: function (data) {

    },
    ReleaseEvent: function (data) {

    },
    RepositoryEvent: function (data) {

    },
    StatusEvent: function (data) {

    },
    TeamEvent: function (data) {

    },
    TeamAddEvent: function (data) {

    },
    WatchEvent: function (data) {

    },
};