
module.exports = {
    mapEventToFunction:function (index) {
        const ActivityArray = [this.CommitCommentEvent, this.CreateEvent,this.DeleteEvent,this.DeploymentEvent,
            this.DeploymentStatusEvent,this.DownloadEvent,this.FollowEvent,this.ForkEvent,this.ForkApplyEvent,this.GistEvent,this.GollumEvent,
            this.IssueCommentEvent,this.IssuesEvent,this.LabelEvent,this.MemberEvent,this.MembershipEvent,this.MilestoneEvent,
            this.OrganizationEvent, this.OrgBlockEvent,this.PageBuildEvent,this.ProjectCardEvent,this.ProjectColumnEvent,this.ProjectEvent,
            this.PublicEvent,this.PullRequestEvent, this.PullRequestReviewEvent,this.PullRequestReviewCommentEvent,this.PushEvent,
            this.ReleaseEvent,this.RepositoryEvent,this.StatusEvent, this.TeamEvent,this.TeamAddEvent,this.WatchEvent
        ];
        if (index === -1){
            // if the event type is not defined
            return null
        }
        return ActivityArray[index]
    },

    getURL(name){
        return `[${name}](https://github.com/${name})`
    },

    formatTime:function (time) {
        let moment = require('moment');
        return `<p style="color:red;">${moment(time).format("h:mm a dddd, MMMM Do YYYY")}</p>`;
    },

    /**
     * @return {string}
     */
    CommitCommentEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `created a [comment](${data.payload.comment.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    CreateEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `created a ${data.payload.ref_type} '${data.payload.ref}' at ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    DeleteEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `delete a ${data.payload.ref_type} '${data.payload.ref}' at ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    DeploymentEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `deployed ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    DeploymentStatusEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `changed the deployment status of ${a.getURL(data.repo.full_name)} to ${data.payload.deployment_status.state} ${time}`
    },
    /**
     * @return {string}
     */
    DownloadEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `downloaded [${data.payload.download.name}](${data.payload.download.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    FollowEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `followed user [${data.payload.target.login}](${data.payload.target.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    ForkEvent:function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `forked [${data.payload.forkee.full_name}](${data.payload.forkee.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    ForkApplyEvent: function (data) {
        // no longer created
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `applied a patch to the fork Queue ${data.payload.head} ${time}`
    },
    /**
     * @return {string}
     */
    GistEvent: function (data) {
        // no longer created
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action}d a [gist](${data.payload.gist.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    GollumEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        const singleOrPlural = data.payload.pages.length === 1? 'page' : 'pages';
        return `created/edited ${data.payload.pages.length} Wiki ${singleOrPlural} for ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    IssueCommentEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a [comment](${data.payload.comment.html_url}) on an [issue](${data.payload.issue.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    IssuesEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} an [issue](${data.payload.issue.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    LabelEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} the label '${data.payload.label.name}' of ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    MemberEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${a.payload.action} [${data.payload.member.login}](${data.payload.member.html_url}) as a collaborator to ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    MembershipEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `[${data.payload.member.login}](${data.payload.member.html_url}) was ${data.payload.action} from team ${data.payload.team.name} ${time}`
    },
    /**
     * @return {string}
     */
    MilestoneEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a [milestone](${data.payload.milestone.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    OrganizationEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `A ${data.payload.action} in organization ${a.getURL('orgs/'+data.payload.organization.login)} ${time}`
    },
    /**
     * @return {string}
     */
    OrgBlockEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} [${data.payload.blocked_user.login}](${data.payload.blocked_user.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    PageBuildEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `I'm too lazy to tell you what he/she did at the following time ${time}`
    },
    /**
     * @return {string}
     */
    ProjectCardEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a project card ${time}`
    },
    /**
     * @return {string}
     */
    ProjectColumnEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a project column ${time}`
    },
    /**
     * @return {string}
     */
    ProjectEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} project '${data.payload.project.name}' in ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    PublicEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `changed ${a.getURL(data.repo.full_name)} to open source ${time}`
    },
    /**
     * @return {string}
     */
    PullRequestEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a [pull request](${data.payload.pull_request.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    PullRequestReviewEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a [pull request review](${data.payload.review.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    PullRequestReviewCommentEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} a [comment](${data.payload.comment.html_url}) on a pull request's unified diff ${time}`
    },
    /**
     * @return {string}
     */
    PushEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        const singleOrPlural = data.payload.size===1? "1 commit": data.payload.size+" commits";
        return `pushed ${singleOrPlural} to ${a.getURL(data.repo.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    ReleaseEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} [release](${data.payload.release.html_url}) ${time}`
    },
    /**
     * @return {string}
     */
    RepositoryEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} ${a.getURL(data.payload.repository.full_name)} ${time}`
    },
    /**
     * @return {string}
     */
    StatusEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `I'm too lazy to tell you what he/she did at the following time ${time}`
    },
    /**
     * @return {string}
     */
    TeamEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} team '${data.payload.team.name}' in organization ${a.getURL('orgs/'+data.payload.organization.login)} ${time}`
    },
    /**
     * @return {string}
     */
    TeamAddEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `added ${a.getURL(data.repo.full_name)} to team '${data.payload.team.name}' ${time}`
    },
    /**
     * @return {string}
     */
    WatchEvent: function (data) {
        const a = require('./Activities');
        const time = a.formatTime(data.created_at);

        return `${data.payload.action} starring ${a.getURL(data.repo.full_name)} ${time}`
    },
};