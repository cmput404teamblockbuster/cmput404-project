import Activities from './Activities'
const ActivityArray = ['CommitCommentEvent', 'CreateEvent','DeleteEvent','DeploymentEvent',
    'DeploymentStatusEvent','DownloadEvent','FollowEvent','ForkEvent','ForkApplyEvent','GistEvent','GollumEvent',
    'IssueCommentEvent','IssuesEvent','LabelEvent','MemberEvent','MembershipEvent','MilestoneEvent',
    'OrganizationEvent', 'OrgBlockEvent','PageBuildEvent','ProjectCardEvent','ProjectColumnEvent','ProjectEvent',
    'PublicEvent','PullRequestEvent', 'PullRequestReviewEvent','PullRequestReviewCommentEvent','PushEvent',
    'ReleaseEvent','RepositoryEvent','StatusEvent', 'TeamEvent','TeamAddEvent','WatchEvent'
];

module.exports = {
    GetMarkDown:function (evetType, data) {
        return Activities.mapEventToFunction(ActivityArray.indexOf(evetType))(data)
    }
};
