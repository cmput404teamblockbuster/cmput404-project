var Activities=require('./Activities');
const ActivityArray = ['CommitCommentEvent', 'CreateEvent','DeleteEvent','DeploymentEvent',
    'DeploymentStatusEvent','DownloadEvent','FollowEvent','ForkEvent','ForkApplyEvent','GistEvent','GollumEvent',
    'IssueCommentEvent','IssuesEvent','LabelEvent','MemberEvent','MembershipEvent','MilestoneEvent',
    'OrganizationEvent', 'OrgBlockEvent','PageBuildEvent','ProjectCardEvent','ProjectColumnEvent','ProjectEvent',
    'PublicEvent','PullRequestEvent', 'PullRequestReviewEvent','PullRequestReviewCommentEvent','PushEvent',
    'ReleaseEvent','RepositoryEvent','StatusEvent', 'TeamEvent','TeamAddEvent','WatchEvent'
];

module.exports = {
    getMarkDown:function (evetType, data) {
        // make sure eventType is in the array
        return Activities.mapEventToFunction(ActivityArray.indexOf(evetType))(data)
    }
};
