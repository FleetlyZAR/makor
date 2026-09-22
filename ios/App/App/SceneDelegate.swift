import UIKit
import Capacitor

// Apps built with the iOS 27 SDK must use the UIScene life cycle, or UIKit
// refuses to launch them. The window and the Capacitor bridge now live in this
// scene, loaded from Main.storyboard through the scene manifest in Info.plist.
//
// Under scenes, iOS delivers opened URLs and Universal Links (WhatsApp, Mail,
// Calendar, the sign in callback) to the scene, not to the AppDelegate. Every
// one is handed to Capacitor's ApplicationDelegateProxy exactly as before, so
// the App plugin's appUrlOpen event and getLaunchUrl keep working unchanged.
class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        // A link that cold started the app arrives here rather than in the
        // callbacks below.
        if let urlContext = connectionOptions.urlContexts.first {
            openURL(urlContext.url, options: urlContext.options)
        }
        for activity in connectionOptions.userActivities {
            continueActivity(activity)
        }
    }

    // A custom scheme link, such as the za.co.makor.app://auth-callback sign in return.
    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        for context in URLContexts {
            openURL(context.url, options: context.options)
        }
    }

    // A Universal Link to makor.co.za tapped while the app is running.
    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        continueActivity(userActivity)
    }

    private func openURL(_ url: URL, options: UIScene.OpenURLOptions) {
        var appOptions: [UIApplication.OpenURLOptionsKey: Any] = [:]
        if let source = options.sourceApplication { appOptions[.sourceApplication] = source }
        if let annotation = options.annotation { appOptions[.annotation] = annotation }
        appOptions[.openInPlace] = options.openInPlace
        _ = ApplicationDelegateProxy.shared.application(UIApplication.shared, open: url, options: appOptions)
    }

    private func continueActivity(_ activity: NSUserActivity) {
        _ = ApplicationDelegateProxy.shared.application(UIApplication.shared, continue: activity, restorationHandler: { _ in })
    }
}
